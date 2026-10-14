"""Long term metric history: one averaged row per minute in SQLite, kept 30 days.

Snapshots are accumulated in memory for the current minute and written when
the minute ends. Queries average minutes into larger buckets for wide ranges.
"""

import os
import sqlite3
import time

from .config import data_dir

KEEP_SECONDS = 31 * 86400
BUCKET = 60

# column -> how the per-minute value is aggregated from snapshots
COLUMNS = {
    "cpu": "avg", "mem": "avg", "swap": "avg", "temp": "avg",
    "down": "avg", "up": "avg", "down_max": "max", "up_max": "max",
    "disk_read": "avg", "disk_write": "avg",
    "latency": "avg", "loss": "avg",
    "battery": "avg", "power": "avg",
}

RANGES = [  # (key, label, seconds, query bucket seconds)
    ("1h", "1 hour", 3600, 60),
    ("6h", "6 hours", 6 * 3600, 300),
    ("24h", "24 hours", 86400, 600),
    ("7d", "7 days", 7 * 86400, 3600),
    ("30d", "30 days", 30 * 86400, 4 * 3600),
]


def _values(snap):
    battery = snap.get("battery") or {}
    loss = snap.get("loss")
    return {
        "cpu": snap["cpu"],
        "mem": snap["mem"]["percent"],
        "swap": snap["swap"]["percent"],
        "temp": snap.get("cpu_temp"),
        "down": snap["net_down"], "up": snap["net_up"],
        "down_max": snap["net_down"], "up_max": snap["net_up"],
        "disk_read": snap["disk_read"], "disk_write": snap["disk_write"],
        "latency": snap.get("latency"),
        "loss": loss * 100 if loss is not None else None,
        "battery": battery.get("percent"),
        "power": battery.get("power"),
    }


class HistoryStore:
    def __init__(self, path=None):
        self.path = path or os.path.join(data_dir(), "history.db")
        self.db = sqlite3.connect(self.path)
        cols = ", ".join(f"{c} REAL" for c in COLUMNS)
        self.db.execute(f"CREATE TABLE IF NOT EXISTS minute (ts INTEGER PRIMARY KEY, {cols})")
        self.db.commit()
        self._bucket = None
        self._acc = {}
        self._last_prune = 0

    # ------------------------------------------------------------- writing
    def add(self, snap):
        bucket = int(snap["time"] // BUCKET) * BUCKET
        if self._bucket is not None and bucket != self._bucket:
            self.flush()
            self._acc = {}
        self._bucket = bucket
        for key, value in _values(snap).items():
            if value is None:
                continue
            total, count, peak = self._acc.get(key, (0.0, 0, value))
            self._acc[key] = (total + value, count + 1, max(peak, value))

    def flush(self):
        """Write the current (possibly partial) minute."""
        if self._bucket is None or not self._acc:
            return
        row = {}
        for key, mode in COLUMNS.items():
            if key in self._acc:
                total, count, peak = self._acc[key]
                row[key] = peak if mode == "max" else total / count
        names = ", ".join(["ts"] + list(row))
        marks = ", ".join("?" * (len(row) + 1))
        try:
            self.db.execute(f"INSERT OR REPLACE INTO minute ({names}) VALUES ({marks})",
                            [self._bucket] + list(row.values()))
            if time.time() - self._last_prune > 3600:
                self.db.execute("DELETE FROM minute WHERE ts < ?", (time.time() - KEEP_SECONDS,))
                self._last_prune = time.time()
            self.db.commit()
        except sqlite3.Error:
            pass

    def close(self):
        self.flush()
        self.db.close()

    # ------------------------------------------------------------- reading
    def query(self, columns, seconds, bucket):
        """{column: [(bucket_ts, value | None), ...]} for the last `seconds`."""
        self.flush()
        start = int(time.time() - seconds) // bucket * bucket
        select = ", ".join(
            f"{'MAX' if COLUMNS[c] == 'max' else 'AVG'}({c})" for c in columns)
        try:
            rows = self.db.execute(
                f"SELECT (ts / {bucket}) * {bucket} AS b, {select} FROM minute WHERE ts >= ? GROUP BY b ORDER BY b",
                (start,)).fetchall()
        except sqlite3.Error:
            rows = []
        return {c: [(r[0], r[i + 1]) for r in rows] for i, c in enumerate(columns)}

    def first_timestamp(self):
        try:
            row = self.db.execute("SELECT MIN(ts) FROM minute").fetchone()
            return row[0] if row else None
        except sqlite3.Error:
            return None
