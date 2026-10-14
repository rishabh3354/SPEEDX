"""Continuous connectivity probing: latency, packet loss, jitter and outages.

Uses unprivileged ICMP echo (Linux "ping sockets") when the kernel allows it
(net.ipv4.ping_group_range), otherwise falls back to timing a TCP handshake.
Runs in its own thread so a slow or dead network never blocks sampling.
"""

import itertools
import socket
import struct
import threading
import time
from collections import deque

from . import system

PROBE_INTERVAL = 2.0     # seconds between probes
RETRY_INTERVAL = 0.5     # faster re-checks after a failed probe
PROBE_TIMEOUT = 1.5
FAIL_THRESHOLD = 3       # consecutive failed probes before declaring an outage
WINDOW = 30              # probes used for loss / jitter (about one minute)
HOSTS = ("1.1.1.1", "8.8.8.8")


class _Pinger:
    def __init__(self):
        self._seq = itertools.count(1)
        self.method = "icmp"
        try:
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP).close()
        except OSError:
            self.method = "tcp"

    def probe(self, host):
        """Round trip time in ms, or None when no reply arrived in time."""
        return self._icmp(host) if self.method == "icmp" else self._tcp(host)

    def _icmp(self, host):
        seq = next(self._seq) & 0xFFFF
        # type 8 (echo request); the kernel fills in identifier and checksum
        packet = struct.pack("!BBHHH", 8, 0, 0, 0, seq) + b"speedx-probe"
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP) as sock:
                start = time.perf_counter()
                deadline = start + PROBE_TIMEOUT
                sock.sendto(packet, (host, 0))
                while True:
                    remaining = deadline - time.perf_counter()
                    if remaining <= 0:
                        return None
                    sock.settimeout(remaining)
                    data = sock.recv(1024)
                    if len(data) >= 8 and data[0] == 0 and struct.unpack("!H", data[6:8])[0] == seq:
                        return (time.perf_counter() - start) * 1000.0
        except (OSError, socket.timeout):
            return None

    @staticmethod
    def _tcp(host):
        start = time.perf_counter()
        try:
            with socket.create_connection((host, 443), timeout=PROBE_TIMEOUT):
                return (time.perf_counter() - start) * 1000.0
        except OSError:
            return None


class ConnectivityMonitor(threading.Thread):
    def __init__(self):
        super().__init__(name="connectivity", daemon=True)
        self._stop = threading.Event()
        self._pinger = _Pinger()
        self.method = "ICMP ping" if self._pinger.method == "icmp" else "TCP handshake"
        self.results = deque(maxlen=WINDOW)   # primary host RTTs (None = lost)
        self.latency = None
        self.online = None                    # None until the first probe completes
        self.outage_since = None              # wall clock start of the current outage
        self.outage_reason = None
        self.events = deque()                 # (kind, start, end, reason) for the GUI thread
        self._fails = 0
        self._first_fail = None
        self._last_probe = None               # (monotonic, wall)

    @property
    def loss(self):
        """Fraction of lost probes over the window, or None before any probe."""
        if not self.results:
            return None
        return sum(1 for r in self.results if r is None) / len(self.results)

    @property
    def jitter(self):
        rtts = [r for r in self.results if r is not None]
        if len(rtts) < 2:
            return None
        return sum(abs(a - b) for a, b in zip(rtts, rtts[1:])) / (len(rtts) - 1)

    def run(self):
        while not self._stop.is_set():
            ok = self._probe_once()
            self._stop.wait(PROBE_INTERVAL if ok else RETRY_INTERVAL)

    def stop(self):
        self._stop.set()

    def _probe_once(self):
        mono, wall = time.monotonic(), time.time()
        if self._last_probe and mono - self._last_probe[0] > PROBE_INTERVAL * 5:
            # The system was suspended (or the thread starved): failures across the gap
            # say nothing about the connection, so close any outage at the last probe.
            if self.outage_since is not None:
                self.events.append(("closed", self.outage_since, self._last_probe[1], self.outage_reason))
                self.outage_since = None
            self._fails = 0
            self.results.clear()
        self._last_probe = (mono, wall)

        has_address = system.local_ip() is not None
        rtt = self._pinger.probe(HOSTS[0]) if has_address else None
        if self._stop.is_set():
            return True
        self.results.append(rtt)
        if rtt is None and has_address:
            rtt = self._pinger.probe(HOSTS[1])  # make sure it is not just one host
        if rtt is not None:
            self.latency = rtt
            self.online = True
            self._fails = 0
            if self.outage_since is not None:
                self.events.append(("restored", self.outage_since, wall, self.outage_reason))
                self.outage_since = None
            return True

        self._fails += 1
        if self._fails == 1:
            self._first_fail = wall
        if self._fails >= FAIL_THRESHOLD and self.outage_since is None:
            self.outage_since = self._first_fail
            self.outage_reason = "Internet unreachable" if has_address else "Network disconnected"
            self.online = False
            self.latency = None
            self.events.append(("lost", self.outage_since, None, self.outage_reason))
        return False
