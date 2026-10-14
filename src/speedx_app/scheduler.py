"""Runs light speed tests automatically on a schedule."""

import datetime as dt
import time

from PyQt5.QtCore import QObject, QTimer

from . import formatting as fmt

CHOICES = [(0, "Off"), (1, "Every hour"), (3, "Every 3 hours"), (6, "Every 6 hours"), (12, "Every 12 hours"),
           (24, "Once a day")]
CHECK_MS = 60_000
STARTUP_DELAY_MS = 120_000      # let the system settle after login
BUSY_BYTES_PER_SEC = 1_000_000  # don't test while something else is downloading
LOW_BATTERY = 20


class SpeedTestScheduler(QObject):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.ctx = ctx
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.check)
        self._ready = False
        QTimer.singleShot(STARTUP_DELAY_MS, self._start)
        QTimer.singleShot(1000, self.update_status)

    def _start(self):
        self._ready = True
        self._timer.start(CHECK_MS)
        self.check()

    def _last_test(self):
        for result in self.ctx.speed_history.results:
            try:
                return dt.datetime.fromisoformat(result["time"]).timestamp()
            except (KeyError, ValueError):
                continue
        return None

    def _label(self, hours):
        return next((text for h, text in CHOICES if h == hours), f"Every {hours} hours").lower()

    def blocker(self):
        """Why a test cannot run right now, or None."""
        ctx = self.ctx
        snap = ctx.monitor.last
        page = ctx.pages[ctx.page_index["speedtest"]]
        if page.is_running():
            return "another test is running"
        if not snap or not snap.get("online"):
            return "no internet connection"
        if ctx.monitor.netinfo.get("metered"):
            return "metered connection (skipped to save data)"
        limit_gb = ctx.config.get("data_limit_gb")
        if limit_gb > 0:
            rx, tx = ctx.usage.cycle_total(ctx.config.get("billing_day"))
            if rx + tx >= 0.9 * limit_gb * 1e9:
                return "close to your monthly data limit"
        recent = list(zip(ctx.monitor.history["down"], ctx.monitor.history["up"]))[-10:]
        if recent and sum(d + u for d, u in recent) / len(recent) > BUSY_BYTES_PER_SEC:
            return "network busy with other traffic"
        battery = snap.get("battery")
        if battery and battery.get("status") == "Discharging" and (battery.get("percent") or 100) < LOW_BATTERY:
            return "battery low"
        return None

    def update_status(self, running=False):
        hours = self.ctx.config.get("auto_test_hours")
        page = self.ctx.pages[self.ctx.page_index["speedtest"]]
        if not hours:
            page.set_auto_status("")
            return
        label = self._label(hours)
        if running:
            page.set_auto_status(f"Automatic tests {label} · running now")
            return
        due = (self._last_test() or 0) + hours * 3600
        wait = due - time.time()
        if wait > 0:
            page.set_auto_status(f"Automatic tests {label} · next in {fmt.duration_precise(wait)}")
        else:
            reason = self.blocker() if self._ready else "starting up"
            page.set_auto_status(f"Automatic tests {label} · waiting: {reason}" if reason
                                 else f"Automatic tests {label} · due now")

    def check(self):
        hours = self.ctx.config.get("auto_test_hours")
        if not hours or not self._ready:
            self.update_status()
            return
        due = (self._last_test() or 0) + hours * 3600
        if time.time() < due or self.blocker():
            self.update_status()
            return
        page = self.ctx.pages[self.ctx.page_index["speedtest"]]
        if page.start_test(automatic=True):
            self.update_status(running=True)
