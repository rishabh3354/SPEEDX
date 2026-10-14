"""Persistent daily network data usage and speed test history."""

import datetime as dt
import json
import os

from .config import data_dir

KEEP_DAYS = 400
KEEP_TESTS = 100


def _load_json(path, default):
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def _save_json(path, data):
    tmp = path + ".tmp"
    try:
        with open(tmp, "w") as fh:
            json.dump(data, fh)
        os.replace(tmp, path)
    except OSError:
        pass


class DataUsageStore:
    """Accumulates received / sent bytes per calendar day.

    Usage is derived from the kernel's per-interface byte counters (cumulative
    since boot), and the last seen counters are saved with the boot time. On the
    next start this recovers traffic that happened while SpeedX was closed:
      * same boot     -> the counter increase since the last save
      * new boot      -> everything since boot (the counters restarted at zero)
    Traffic between the last save and a shutdown is the only part that is lost,
    so the store is saved every few seconds and on exit.
    """

    BOOT_TOLERANCE = 5  # seconds; boot_time() can drift slightly between reads

    def __init__(self):
        self.path = os.path.join(data_dir(), "data_usage.json")
        raw = _load_json(self.path, {})
        self.days = {k: list(v) for k, v in raw.get("days", {}).items() if len(v) == 2}
        state = raw.get("counters") or {}
        self._saved_boot = state.get("boot")
        self._ifaces = {k: list(v) for k, v in state.get("ifaces", {}).items() if len(v) == 2}
        self._started = False
        self.recovered = 0  # bytes recorded at startup that were used while SpeedX was closed
        self._dirty = False

    def _add_today(self, rx, tx):
        if not rx and not tx:
            return
        day = self.days.setdefault(dt.date.today().isoformat(), [0, 0])
        day[0] += int(rx)
        day[1] += int(tx)

    def update(self, counters, boot_time):
        """Feed absolute counters {interface: (rx, tx)} of physical interfaces."""
        if not counters:
            return
        if not self._started:
            self._started = True
            if self._saved_boot is None:
                # first run (or upgrade from a version without counters): baseline only
                self._ifaces = {k: list(v) for k, v in counters.items()}
                self._saved_boot = boot_time
                self._dirty = True
                return
            if abs(self._saved_boot - boot_time) > self.BOOT_TOLERANCE:
                self._ifaces = {}  # rebooted: every interface counted from zero
            self._saved_boot = boot_time
            rx, tx = self._diff(counters)
            self.recovered = rx + tx
            self._add_today(rx, tx)
            self._dirty = True
            return
        rx, tx = self._diff(counters)
        self._add_today(rx, tx)
        self._dirty = True

    def _diff(self, counters):
        rx = tx = 0
        for name, (r, t) in counters.items():
            prev = self._ifaces.get(name)
            if prev is None or r < prev[0] or t < prev[1]:
                # new interface, or its counters were reset (driver reload, re-plugged
                # USB modem): everything it has counted so far is new traffic
                prev = (0, 0)
            rx += r - prev[0]
            tx += t - prev[1]
            self._ifaces[name] = [r, t]
        return rx, tx

    def save(self):
        if not self._dirty:
            return
        cutoff = (dt.date.today() - dt.timedelta(days=KEEP_DAYS)).isoformat()
        self.days = {k: v for k, v in self.days.items() if k >= cutoff}
        _save_json(self.path, {
            "days": self.days,
            "counters": {"boot": self._saved_boot, "ifaces": self._ifaces},
        })
        self._dirty = False

    def reset(self):
        self.days = {}
        self.recovered = 0
        self._dirty = True
        self.save()

    def day(self, date):
        rx, tx = self.days.get(date.isoformat(), (0, 0))
        return rx, tx

    def total_between(self, start, end):
        """Sum of (rx, tx) for start <= date <= end."""
        rx = tx = 0
        s, e = start.isoformat(), end.isoformat()
        for key, (r, t) in self.days.items():
            if s <= key <= e:
                rx += r
                tx += t
        return rx, tx

    def last_days(self, count):
        today = dt.date.today()
        result = []
        for offset in range(count - 1, -1, -1):
            d = today - dt.timedelta(days=offset)
            rx, tx = self.day(d)
            result.append((d, rx, tx))
        return result

    @staticmethod
    def cycle_start(billing_day, today=None):
        today = today or dt.date.today()
        billing_day = max(1, min(28, int(billing_day)))
        if today.day >= billing_day:
            return today.replace(day=billing_day)
        first = today.replace(day=1)
        prev_month = first - dt.timedelta(days=1)
        return prev_month.replace(day=billing_day)

    def cycle_total(self, billing_day):
        start = self.cycle_start(billing_day)
        return self.total_between(start, dt.date.today())


class SpeedTestHistory:
    def __init__(self):
        self.path = os.path.join(data_dir(), "speed_tests.json")
        self.results = _load_json(self.path, [])
        if not isinstance(self.results, list):
            self.results = []

    def add(self, result):
        self.results.insert(0, result)
        del self.results[KEEP_TESTS:]
        _save_json(self.path, self.results)

    def clear(self):
        self.results = []
        _save_json(self.path, self.results)


class OutageLog:
    """Completed internet outages: dicts with start / end (epoch seconds) and reason."""

    KEEP = 500

    def __init__(self):
        self.path = os.path.join(data_dir(), "outages.json")
        data = _load_json(self.path, [])
        self.items = [o for o in data if isinstance(o, dict) and "start" in o and "end" in o] \
            if isinstance(data, list) else []

    def add(self, start, end, reason, note=""):
        if end - start < 1:
            return
        self.items.insert(0, {"start": start, "end": end, "reason": reason, "note": note})
        del self.items[self.KEEP:]
        _save_json(self.path, self.items)

    def since(self, seconds_ago):
        cutoff = dt.datetime.now().timestamp() - seconds_ago
        return [o for o in self.items if o["end"] >= cutoff]

    def clear(self):
        self.items = []
        _save_json(self.path, self.items)
