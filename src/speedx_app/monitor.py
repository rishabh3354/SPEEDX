"""Background sampling of system statistics.

A single worker running in its own QThread collects every metric on a timer and
emits a plain dict snapshot. The GUI thread never blocks on psutil calls.
"""

import time
from collections import deque

import psutil
from PyQt5.QtCore import QObject, Qt, QThread, QTimer, pyqtSignal, pyqtSlot

from . import system
from .apps import group_for
from .battery import battery_info, has_battery
from .connectivity import ConnectivityMonitor
from .netinfo import NetworkInfo

HISTORY_SECONDS = 120
PARTITION_INTERVAL = 15.0
NETINFO_INTERVAL = 5.0
BLOCKED_RETRY = 60.0      # seconds before re-trying a sensor the sandbox denied


class _Sampler(QObject):
    sampled = pyqtSignal(object)

    def __init__(self, interval, interface):
        super().__init__()
        self.interval = interval
        self.interface = interface
        self.want_processes = False
        self._timer = None
        self._last_time = None
        self._last_net = None
        self._last_disk = None
        self._last_partitions = 0.0
        self._last_netinfo = 0.0
        self._temp_retry = 0.0    # when an unreadable sensor may be tried again
        self._disk_retry = 0.0
        self._tick = 0
        self._ncpu = psutil.cpu_count() or 1
        self._physical = {}
        self._groups = {}  # pid -> app name (a process never changes app)
        self._has_battery = has_battery()
        self.probe = ConnectivityMonitor()
        self._netinfo = NetworkInfo()

    @pyqtSlot()
    def start(self):
        self.probe.start()
        psutil.cpu_percent(percpu=True)  # prime the counters
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._sample)
        self._timer.start(int(self.interval * 1000))
        QTimer.singleShot(250, self._sample)

    @pyqtSlot()
    def stop(self):
        self.probe.stop()
        if self._timer:
            self._timer.stop()

    @pyqtSlot(float)
    def set_interval(self, seconds):
        self.interval = seconds
        if self._timer:
            self._timer.start(int(seconds * 1000))

    @pyqtSlot(str)
    def set_interface(self, name):
        self.interface = name
        self._last_net = None

    def _temperature(self, now):
        """CPU temperature, backing off when no sensor is readable.

        Without the snap hardware-observe interface every sensor read is denied
        (and logged by AppArmor), so don't retry every second.
        """
        if now < self._temp_retry:
            return None
        temp = system.cpu_temperature()
        if temp is None:
            self._temp_retry = now + BLOCKED_RETRY
        return temp

    def _is_physical(self, name):
        if name not in self._physical:
            self._physical[name] = system.is_physical(name)
        return self._physical[name]

    def _net_counters(self):
        """((selected rx, tx, physical rx, tx), {physical iface: (rx, tx)}) since boot."""
        try:
            per_nic = psutil.net_io_counters(pernic=True)
        except OSError:
            return None, {}
        physical = {name: (c.bytes_recv, c.bytes_sent) for name, c in per_nic.items() if self._is_physical(name)}
        all_rx = sum(v[0] for v in physical.values())
        all_tx = sum(v[1] for v in physical.values())
        if self.interface and self.interface in per_nic:
            c = per_nic[self.interface]
            sel = (c.bytes_recv, c.bytes_sent)
        elif self.interface:
            sel = (0, 0)
        else:
            sel = (all_rx, all_tx)
        return sel + (all_rx, all_tx), physical

    def _processes(self):
        rows = []
        seen = set()
        attrs = ["pid", "name", "username", "memory_info", "memory_percent", "status"]
        for proc in psutil.process_iter(attrs):
            try:
                info = proc.info
                cpu = proc.cpu_percent(None) / self._ncpu
                rss = info["memory_info"].rss if info["memory_info"] else 0
                pid, name = info["pid"], info["name"] or "?"
                seen.add(pid)
                if pid not in self._groups:
                    self._groups[pid] = group_for(pid, name)
                rows.append((
                    pid,
                    name,
                    info["username"] or "",
                    cpu,
                    rss,
                    info["memory_percent"] or 0.0,
                    info["status"] or "",
                    self._groups[pid],
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        for pid in set(self._groups) - seen:
            del self._groups[pid]
        return rows

    @pyqtSlot()
    def _sample(self):
        now = time.monotonic()
        dt = (now - self._last_time) if self._last_time else self.interval
        dt = max(dt, 0.05)
        self._last_time = now
        self._tick += 1

        cores = psutil.cpu_percent(percpu=True)
        snap = {
            "time": time.time(),
            "cpu": sum(cores) / len(cores) if cores else 0.0,
            "cpu_cores": cores,
            "cpu_freq": system.cpu_frequency(),
            "cpu_temp": self._temperature(now),
            "load": system.load_average(),
            "uptime": time.time() - psutil.boot_time(),
            "latency": self.probe.latency,
            "online": self.probe.online,
            "loss": self.probe.loss,
            "jitter": self.probe.jitter,
            "outage_since": self.probe.outage_since,
            "outage_reason": self.probe.outage_reason,
            "events": [],
            "netinfo": None,
            "battery": battery_info() if self._has_battery else None,
            "boot_time": psutil.boot_time(),
            "processes": None,
            "partitions": None,
        }
        while self.probe.events:
            snap["events"].append(self.probe.events.popleft())

        vm = psutil.virtual_memory()
        snap["mem"] = {
            "total": vm.total,
            "used": vm.total - vm.available,
            "available": vm.available,
            "percent": vm.percent,
            "cached": getattr(vm, "cached", 0) + getattr(vm, "buffers", 0),
        }
        sw = psutil.swap_memory()
        snap["swap"] = {"total": sw.total, "used": sw.used, "percent": sw.percent}

        down = up = rx_all = tx_all = 0.0
        net, physical = self._net_counters()
        snap["net_counters"] = physical
        if net and self._last_net:
            deltas = [max(0, a - b) for a, b in zip(net, self._last_net)]
            down, up = deltas[0] / dt, deltas[1] / dt
            rx_all, tx_all = deltas[2], deltas[3]
        if net:
            self._last_net = net
        snap.update(net_down=down, net_up=up, net_rx_delta=rx_all, net_tx_delta=tx_all)

        read = write = 0.0
        disk = None
        if now >= self._disk_retry:
            try:
                disk = psutil.disk_io_counters()
            except (OSError, RuntimeError):
                # e.g. /proc/diskstats blocked in a snap without hardware-observe
                self._disk_retry = now + BLOCKED_RETRY
        if disk and self._last_disk:
            read = max(0, disk.read_bytes - self._last_disk.read_bytes) / dt
            write = max(0, disk.write_bytes - self._last_disk.write_bytes) / dt
        if disk:
            self._last_disk = disk
        snap.update(disk_read=read, disk_write=write)

        if now - self._last_netinfo >= NETINFO_INTERVAL or self._tick == 1:
            self._last_netinfo = now
            snap["netinfo"] = self._netinfo.query()

        if self.want_processes:
            snap["processes"] = self._processes()
        if now - self._last_partitions >= PARTITION_INTERVAL or self._tick == 1:
            self._last_partitions = now
            snap["partitions"] = system.disk_partitions()

        self.sampled.emit(snap)


class Monitor(QObject):
    """Owns the sampler thread and keeps short histories for the charts."""

    updated = pyqtSignal(object)
    _start_worker = pyqtSignal()
    _stop_worker = pyqtSignal()
    _interval_changed = pyqtSignal(float)
    _interface_changed = pyqtSignal(str)

    def __init__(self, interval=1.0, interface=""):
        super().__init__()
        self.interval = interval
        self.info = system.static_info()
        self.last = None
        self.partitions = []
        self.netinfo = {}
        self.processes = []
        self._reset_history()
        self.session_rx = 0
        self.session_tx = 0
        self.peak_down = 0.0
        self.peak_up = 0.0

        self._thread = QThread()
        self._worker = _Sampler(interval, interface)
        self._worker.moveToThread(self._thread)
        self._worker.sampled.connect(self._on_sample)
        self._start_worker.connect(self._worker.start)
        self._stop_worker.connect(self._worker.stop, Qt.BlockingQueuedConnection)
        self._interval_changed.connect(self._worker.set_interval)
        self._interface_changed.connect(self._worker.set_interface)

    def _reset_history(self):
        n = max(30, int(HISTORY_SECONDS / max(self.interval, 0.25)))
        self.history = {key: deque(maxlen=n) for key in (
            "cpu", "mem", "swap", "down", "up", "disk_read", "disk_write", "temp", "power")}
        self.core_history = []
        self.latency_history = deque(maxlen=60)

    def start(self):
        self._thread.start()
        self._start_worker.emit()

    def stop(self):
        if self._thread.isRunning():
            self._stop_worker.emit()
        self._thread.quit()
        self._thread.wait(2000)

    def set_interval(self, seconds):
        self.interval = seconds
        self._reset_history()
        self._interval_changed.emit(float(seconds))

    def set_interface(self, name):
        self.peak_down = self.peak_up = 0.0
        for key in ("down", "up"):
            self.history[key].clear()
        self._interface_changed.emit(name)

    @property
    def probe_method(self):
        return self._worker.probe.method

    def set_want_processes(self, wanted):
        self._worker.want_processes = wanted

    def _on_sample(self, snap):
        h = self.history
        h["cpu"].append(snap["cpu"])
        h["mem"].append(snap["mem"]["percent"])
        h["swap"].append(snap["swap"]["percent"])
        h["down"].append(snap["net_down"])
        h["up"].append(snap["net_up"])
        h["disk_read"].append(snap["disk_read"])
        h["disk_write"].append(snap["disk_write"])
        if snap["cpu_temp"] is not None:
            h["temp"].append(snap["cpu_temp"])
        battery = snap["battery"]
        if battery and battery.get("power") is not None:
            h["power"].append(battery["power"])

        cores = snap["cpu_cores"]
        if len(self.core_history) != len(cores):
            self.core_history = [deque(maxlen=h["cpu"].maxlen) for _ in cores]
        for buf, value in zip(self.core_history, cores):
            buf.append(value)

        prev_latency = self.last.get("latency") if self.last else None
        if snap["latency"] is not None and snap["latency"] != prev_latency:
            self.latency_history.append(snap["latency"])

        self.session_rx += snap["net_rx_delta"]
        self.session_tx += snap["net_tx_delta"]
        self.peak_down = max(self.peak_down, snap["net_down"])
        self.peak_up = max(self.peak_up, snap["net_up"])
        if snap["partitions"] is not None:
            self.partitions = snap["partitions"]
        if snap["netinfo"] is not None:
            self.netinfo = snap["netinfo"]
        if snap["processes"] is not None:
            self.processes = snap["processes"]
        self.last = snap
        self.updated.emit(snap)
