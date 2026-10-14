"""Threshold alerts delivered as desktop notifications."""

import time

from PyQt5.QtCore import QMetaType

from . import APP_NAME
from . import formatting as fmt

try:
    from PyQt5.QtDBus import QDBusArgument, QDBusConnection, QDBusInterface
except ImportError:  # QtDBus is optional
    QDBusConnection = None

COOLDOWN = 10 * 60  # seconds between repeats of the same alert
CPU_SUSTAIN = 30    # seconds CPU must stay high before alerting


class Notifier:
    def __init__(self, tray=None):
        self.tray = tray
        self._dbus = None
        if QDBusConnection is not None:
            bus = QDBusConnection.sessionBus()
            if bus.isConnected():
                iface = QDBusInterface("org.freedesktop.Notifications", "/org/freedesktop/Notifications",
                                       "org.freedesktop.Notifications", bus)
                if iface.isValid():
                    self._dbus = iface

    def notify(self, title, message):
        if self._dbus is not None:
            reply = self._dbus.call("Notify", APP_NAME, QDBusArgument(0, QMetaType.UInt), "speedx", title,
                                    message, QDBusArgument([], QMetaType.QStringList), {}, 8000)
            if not reply.errorName():
                return
        if self.tray is not None:
            self.tray.show_message(title, message)


class AlertManager:
    def __init__(self, config, usage, notifier):
        self.config = config
        self.usage = usage
        self.notifier = notifier
        self._last = {}
        self._cpu_high_since = None
        self._limit_sent = {}  # billing cycle start -> highest level notified

    def _fire(self, key, title, message):
        now = time.monotonic()
        if now - self._last.get(key, -COOLDOWN) < COOLDOWN:
            return
        self._last[key] = now
        self.notifier.notify(title, message)

    def check(self, snap):
        cfg = self.config
        if not cfg.get("alerts_enabled"):
            return
        cpu = snap["cpu"]
        if cpu >= cfg.get("alert_cpu"):
            self._cpu_high_since = self._cpu_high_since or time.monotonic()
            if time.monotonic() - self._cpu_high_since >= CPU_SUSTAIN:
                self._fire("cpu", "High CPU usage", f"CPU usage has been above {cfg.get('alert_cpu')}% "
                           f"for {CPU_SUSTAIN} seconds (now {cpu:.0f}%).")
        else:
            self._cpu_high_since = None

        mem = snap["mem"]["percent"]
        if mem >= cfg.get("alert_ram"):
            self._fire("ram", "Memory almost full", f"RAM usage is at {mem:.0f}%. "
                       "Close some applications to keep your system responsive.")

        temp = snap["cpu_temp"]
        if temp is not None and temp >= cfg.get("alert_temp"):
            self._fire("temp", "CPU is running hot",
                       f"CPU temperature reached {fmt.temperature(temp, cfg.get('temp_unit'))}.")

        self._check_data_limit()

    def _check_data_limit(self):
        limit_gb = self.config.get("data_limit_gb")
        if limit_gb <= 0:
            return
        billing_day = self.config.get("billing_day")
        rx, tx = self.usage.cycle_total(billing_day)
        frac = (rx + tx) / (limit_gb * 1e9)
        level = 100 if frac >= 1 else 80 if frac >= 0.8 else None
        if level is None:
            return
        cycle = self.usage.cycle_start(billing_day)
        if self._limit_sent.get(cycle, 0) >= level:
            return
        self._limit_sent[cycle] = level
        if level == 100:
            self.notifier.notify("Data limit reached", f"You have used your {limit_gb:g} GB monthly data limit.")
        else:
            self.notifier.notify("80% of data limit used",
                                 f"You have used {fmt.data(rx + tx)} of your {limit_gb:g} GB monthly limit.")
