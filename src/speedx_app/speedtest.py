"""Internet speed test.

Primary provider: Cloudflare's public speed test endpoints. If Cloudflare cannot
be reached, the nearest LibreSpeed community server is used instead.

Latency is measured with small requests on a warm connection, download and
upload throughput with several parallel streams over a fixed duration (or until
a data cap is reached, for the lighter scheduled tests).
"""

import concurrent.futures as cf
import datetime as dt
import http.client
import json
import os
import socket
import statistics
import struct
import threading
import time
import urllib.parse

from PyQt5.QtCore import QThread, pyqtSignal

from . import APP_NAME, VERSION

HEADERS = {"User-Agent": f"{APP_NAME}/{VERSION}"}
TIMEOUT = 10
WARMUP_SECONDS = 1.5
CHUNK = 64 * 1024
REQUEST_BYTES = 25_000_000
UPLOAD_BODY = 2_000_000
LIBRESPEED_LIST = "https://librespeed.org/backend-servers/servers.php"

PROFILES = {
    # manual test: accurate, uses more data on fast connections
    "full": dict(ping_samples=12, dl_streams=4, dl_seconds=10.0, dl_cap=None,
                 ul_streams=3, ul_seconds=8.0, ul_cap=None),
    # scheduled test: shorter and capped at ~55 MB in total
    "light": dict(ping_samples=8, dl_streams=3, dl_seconds=6.0, dl_cap=40_000_000,
                  ul_streams=2, ul_seconds=5.0, ul_cap=15_000_000),
}


TCP_INFO_BYTES_ACKED = 120  # offset of tcpi_bytes_acked (u64) in Linux struct tcp_info


def _bytes_acked(sock):
    """Bytes the peer has acknowledged on this TCP socket (Linux), else None.

    Upload speed must be measured from acknowledged data: bytes written to the
    socket can sit in multi-megabyte kernel send buffers and would inflate the
    result, especially for short tests.
    """
    try:
        raw = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_INFO, 192)
    except (OSError, AttributeError):
        return None
    if len(raw) < TCP_INFO_BYTES_ACKED + 8:
        return None
    return struct.unpack_from("Q", raw, TCP_INFO_BYTES_ACKED)[0]


class SpeedTestCancelled(Exception):
    pass


class Server:
    def __init__(self, provider, base_url, ping_path, dl_path, ul_path, name, location="", chunked_mb=False):
        parts = urllib.parse.urlsplit(base_url)
        self.provider = provider
        self.https = parts.scheme != "http"
        self.host = parts.netloc
        self.base = parts.path.rstrip("/")
        self.ping_path = self._join(ping_path)
        self.dl_base = self._join(dl_path)
        self.ul_path = self._join(ul_path)
        self.name = name
        self.location = location
        self.chunked_mb = chunked_mb

    def _join(self, path):
        if path.startswith("/") and not self.base:
            return path
        return f"{self.base}/{path.lstrip('/')}"

    def connect(self):
        cls = http.client.HTTPSConnection if self.https else http.client.HTTPConnection
        return cls(self.host, timeout=TIMEOUT)

    def download_path(self, nbytes):
        if self.chunked_mb:  # LibreSpeed: size in 1 MiB chunks
            sep = "&" if "?" in self.dl_base else "?"
            return f"{self.dl_base}{sep}ckSize={max(1, min(1024, nbytes // 1048576))}"
        return f"{self.dl_base}{nbytes}"


def _get(url, timeout=TIMEOUT):
    parts = urllib.parse.urlsplit(url)
    cls = http.client.HTTPSConnection if parts.scheme == "https" else http.client.HTTPConnection
    conn = cls(parts.netloc, timeout=timeout)
    try:
        conn.request("GET", parts.path + (f"?{parts.query}" if parts.query else ""), headers=HEADERS)
        resp = conn.getresponse()
        body = resp.read()
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status}")
        return body
    finally:
        conn.close()


class SpeedTest(QThread):
    # phase ("latency" | "download" | "upload"), live value, phase progress 0..1
    progress = pyqtSignal(str, float, float)
    phase_done = pyqtSignal(str, float)
    server_info = pyqtSignal(dict)
    completed = pyqtSignal(dict)
    failed = pyqtSignal(str)

    def __init__(self, profile="full", automatic=False, parent=None):
        super().__init__(parent)
        self.profile = PROFILES[profile]
        self.profile_name = profile
        self.automatic = automatic
        self._cancel = False
        self._lock = threading.Lock()
        self._bytes = 0

    def cancel(self):
        self._cancel = True

    def _check_cancel(self):
        if self._cancel:
            raise SpeedTestCancelled()

    def _add(self, n):
        with self._lock:
            self._bytes += n

    # --------------------------------------------------------------- servers
    def _cloudflare(self):
        info = {}
        try:
            for line in _get("https://speed.cloudflare.com/cdn-cgi/trace").decode(errors="replace").splitlines():
                if "=" in line:
                    key, value = line.split("=", 1)
                    info[key] = value
        except (OSError, http.client.HTTPException, RuntimeError):
            pass
        server = Server("Cloudflare", "https://speed.cloudflare.com", "/__down?bytes=0", "/__down?bytes=",
                        "/__up", f"Cloudflare {info.get('colo', '')}".strip(), info.get("loc", ""))
        return server, info.get("ip", "")

    def _librespeed(self):
        servers = json.loads(_get(LIBRESPEED_LIST))

        def candidate(entry):
            base = entry["server"]
            if base.startswith("//"):
                base = "https:" + base
            server = Server("LibreSpeed", base, entry["pingURL"], entry["dlURL"], entry["ulURL"],
                            entry.get("name", base), chunked_mb=True)
            start = time.perf_counter()
            conn = server.connect()
            try:
                conn.request("GET", server.ping_path, headers=HEADERS)
                conn.getresponse().read()
                start = time.perf_counter()  # second request on the warm connection
                conn.request("GET", server.ping_path, headers=HEADERS)
                resp = conn.getresponse()
                resp.read()
                if resp.status != 200:
                    return None
                return time.perf_counter() - start, server
            finally:
                conn.close()

        best = None
        with cf.ThreadPoolExecutor(max_workers=12) as pool:
            futures = [pool.submit(candidate, s) for s in servers if isinstance(s, dict) and "server" in s]
            for future in cf.as_completed(futures, timeout=15):
                try:
                    result = future.result()
                except Exception:  # noqa: BLE001 - skip unreachable servers
                    continue
                if result and (best is None or result[0] < best[0]):
                    best = result
        if best is None:
            raise RuntimeError("No LibreSpeed server reachable")
        return best[1], ""

    # ---------------------------------------------------------------- phases
    def _latency(self, server, samples_wanted):
        conn = server.connect()
        samples = []
        try:
            for i in range(samples_wanted + 1):
                self._check_cancel()
                start = time.perf_counter()
                conn.request("GET", server.ping_path, headers=HEADERS)
                resp = conn.getresponse()
                resp.read()
                elapsed = (time.perf_counter() - start) * 1000.0
                if resp.status != 200:
                    raise RuntimeError(f"Server returned HTTP {resp.status}")
                if i == 0:
                    continue  # first request includes connection setup
                samples.append(elapsed)
                self.progress.emit("latency", elapsed, i / samples_wanted)
        finally:
            conn.close()
        ping = statistics.median(samples)
        jitter = statistics.mean(abs(a - b) for a, b in zip(samples, samples[1:])) if len(samples) > 1 else 0.0
        return ping, jitter

    def _download_worker(self, stop, errors, server):
        try:
            conn = server.connect()
            while not stop.is_set():
                conn.request("GET", server.download_path(REQUEST_BYTES), headers=HEADERS)
                resp = conn.getresponse()
                if resp.status != 200:
                    raise RuntimeError(f"Server returned HTTP {resp.status}")
                while not stop.is_set():
                    chunk = resp.read(CHUNK)
                    if not chunk:
                        break
                    self._add(len(chunk))
            conn.close()
        except Exception as exc:  # noqa: BLE001 - reported to the user
            errors.append(exc)

    def _upload_worker(self, stop, errors, server, payload):
        try:
            conn = server.connect()
            view = memoryview(payload)
            sock = None
            counted = 0  # acknowledged bytes already added for the current socket

            def account(sent_now):
                nonlocal counted
                acked = _bytes_acked(sock) if sock is not None else None
                if acked is None:
                    self._add(sent_now)  # no TCP_INFO: fall back to bytes written
                elif acked > counted:
                    self._add(acked - counted)
                    counted = acked

            while not stop.is_set():
                conn.putrequest("POST", server.ul_path)
                conn.putheader("Content-Type", "application/octet-stream")
                conn.putheader("Content-Length", str(len(payload)))
                for key, value in HEADERS.items():
                    conn.putheader(key, value)
                conn.endheaders()
                if conn.sock is not sock:  # (re)connected: new counters
                    sock, counted = conn.sock, 0
                    if _bytes_acked(sock) is not None:
                        counted = _bytes_acked(sock)  # skip handshake / headers
                for offset in range(0, len(payload), CHUNK):
                    if stop.is_set():
                        break
                    piece = view[offset:offset + CHUNK]
                    conn.send(piece)
                    account(len(piece))
                if stop.is_set():
                    break
                resp = conn.getresponse()
                resp.read()
                account(0)
                if resp.status != 200:
                    raise RuntimeError(f"Server returned HTTP {resp.status}")
            conn.close()
        except Exception as exc:  # noqa: BLE001 - reported to the user
            errors.append(exc)

    def _throughput(self, phase, streams, seconds, cap, target, args=()):
        """Returns (Mbps, bytes transferred)."""
        self._bytes = 0
        stop = threading.Event()
        errors = []
        threads = [threading.Thread(target=target, args=(stop, errors) + args, daemon=True)
                   for _ in range(streams)]
        for t in threads:
            t.start()
        start = time.perf_counter()
        samples = [(0.0, 0)]
        try:
            while True:
                time.sleep(0.2)
                self._check_cancel()
                elapsed = time.perf_counter() - start
                total = self._bytes
                samples.append((elapsed, total))
                t0, b0 = next(((t, b) for t, b in samples if t >= elapsed - 1.0), samples[0])
                live = (total - b0) * 8 / max(elapsed - t0, 0.05) / 1e6
                done = max(elapsed / seconds, total / cap if cap else 0)
                self.progress.emit(phase, live, min(1.0, done))
                if done >= 1.0:
                    break
                if errors and not any(t.is_alive() for t in threads):
                    break
        finally:
            stop.set()

        elapsed, total = samples[-1]
        if total == 0:
            raise errors[0] if errors else RuntimeError("No data transferred")
        tw, bw = next(((t, b) for t, b in samples if t >= WARMUP_SECONDS), samples[0])
        if elapsed - tw < 1.0:
            tw, bw = samples[0]
        return (total - bw) * 8 / max(elapsed - tw, 0.05) / 1e6, total

    # ------------------------------------------------------------------- run
    def run(self):
        p = self.profile
        try:
            server = ip = None
            ping = jitter = None
            errors = []
            for pick in (self._cloudflare, self._librespeed):
                self._check_cancel()
                try:
                    server, ip = pick()
                    self.server_info.emit({"server": server.name, "location": server.location, "ip": ip,
                                           "provider": server.provider})
                    ping, jitter = self._latency(server, p["ping_samples"])
                    break
                except SpeedTestCancelled:
                    raise
                except Exception as exc:  # noqa: BLE001 - try the next provider
                    errors.append(f"{pick.__name__.strip('_')}: {exc}")
                    server = None
            if server is None:
                raise RuntimeError("no speed test server reachable (" + "; ".join(errors) + ")")
            self.phase_done.emit("latency", ping)

            download, dl_bytes = self._throughput("download", p["dl_streams"], p["dl_seconds"], p["dl_cap"],
                                                  self._download_worker, (server,))
            self.phase_done.emit("download", download)

            payload = os.urandom(UPLOAD_BODY)
            upload, ul_bytes = self._throughput("upload", p["ul_streams"], p["ul_seconds"], p["ul_cap"],
                                                self._upload_worker, (server, payload))
            self.phase_done.emit("upload", upload)

            self.completed.emit({
                "time": dt.datetime.now().isoformat(timespec="seconds"),
                "ping": round(ping, 1),
                "jitter": round(jitter, 1),
                "download": round(download, 2),
                "upload": round(upload, 2),
                "server": server.name,
                "location": server.location,
                "provider": server.provider,
                "ip": ip or "",
                "data_used": dl_bytes + ul_bytes,
                "automatic": self.automatic,
                "profile": self.profile_name,
            })
        except SpeedTestCancelled:
            self.failed.emit("cancelled")
        except Exception as exc:  # noqa: BLE001 - shown to the user
            self.failed.emit(str(exc) or exc.__class__.__name__)
