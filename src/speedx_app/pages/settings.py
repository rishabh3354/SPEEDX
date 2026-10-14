from PyQt5.QtWidgets import (QComboBox, QDoubleSpinBox, QHBoxLayout, QMessageBox, QPushButton, QSpinBox,
                             QVBoxLayout, QWidget)

from .. import autostart
from ..scheduler import CHOICES as AUTO_TEST_CHOICES
from ..tray import CONTENT_CHOICES
from ..widgets.common import Card, Page, Toggle, divider, label

INTERVALS = [(0.5, "0.5 seconds"), (1.0, "1 second"), (2.0, "2 seconds"), (3.0, "3 seconds"), (5.0, "5 seconds")]


class _Row(QWidget):
    def __init__(self, title, description, control, parent=None):
        super().__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 2, 0, 2)
        lay.setSpacing(16)
        texts = QVBoxLayout()
        texts.setSpacing(2)
        texts.addWidget(label(title, "Value"))
        if description:
            texts.addWidget(label(description, "Faint", wrap=True))
        lay.addLayout(texts, 1)
        lay.addWidget(control)


class SettingsPage(Page):
    def __init__(self, ctx):
        super().__init__("Settings", "Make SpeedX work the way you like")
        self.ctx = ctx
        cfg = ctx.config
        tray = ctx.tray

        # appearance & behaviour
        general = Card("General")
        self.theme_box = self._combo([("dark", "Dark"), ("light", "Light"), ("system", "Follow system")],
                                     cfg.get("theme"), lambda v: cfg.set("theme", v))
        self._add(general, "Theme", "Color scheme of the app", self.theme_box)
        self._add(general, "Launch at login", "Start SpeedX automatically when you sign in",
                  self._toggle("autostart", self._set_autostart))
        self._add(general, "Start minimized", "Open in the background (tray or mini meter) instead of the window",
                  self._toggle("start_minimized"))
        self.add(general)

        # system tray
        tray_card = Card("System tray", "Live speed in your panel, next to the clock and battery"
                         if tray.available else "No system tray detected on this desktop")
        speed_toggle = self._toggle("tray_speed")
        speed_toggle.setEnabled(tray.available)
        self._add(tray_card, "Show live speed in the tray",
                  "See your current internet speed at a glance without opening SpeedX", speed_toggle)
        content = self._combo(CONTENT_CHOICES, cfg.get("tray_content"), lambda v: cfg.set("tray_content", v))
        content.setEnabled(tray.available)
        self._add(tray_card, "Tray shows", None, content)
        if tray.supports_label:
            self._add(tray_card, "Display style",
                      "Text beside the icon works on Ubuntu, GNOME, XFCE and MATE. KDE shows only the icon, "
                      "so use “Inside the icon” there",
                      self._combo([("auto", "Automatic"), ("label", "Text beside the icon"),
                                   ("icon", "Inside the icon")],
                                  cfg.get("tray_style"), lambda v: cfg.set("tray_style", v)))
        close_toggle = self._toggle("close_to_tray")
        close_toggle.setEnabled(tray.available)
        self._add(tray_card, "Keep running in the tray", "Closing the window keeps SpeedX running in the background",
                  close_toggle)
        self.add(tray_card)

        # monitoring
        monitoring = Card("Monitoring")
        self._add(monitoring, "Update interval", "How often statistics refresh. Faster uses slightly more CPU",
                  self._combo(INTERVALS, cfg.get("interval"), lambda v: cfg.set("interval", v)))
        self._add(monitoring, "Speed units", "Show transfer rates in bytes (MB/s) or bits (Mbps)",
                  self._combo([("bytes", "Bytes  (KB/s, MB/s)"), ("bits", "Bits  (Kbps, Mbps)")],
                              cfg.get("speed_unit"), lambda v: cfg.set("speed_unit", v)))
        self._add(monitoring, "Temperature unit", None,
                  self._combo([("C", "Celsius (°C)"), ("F", "Fahrenheit (°F)")],
                              cfg.get("temp_unit"), lambda v: cfg.set("temp_unit", v)))
        self.add(monitoring)

        # automatic speed tests
        tests = Card("Automatic speed tests", "Track your internet speed over time to spot problems with your ISP")
        self._add(tests, "Run a speed test automatically",
                  "Light tests use about 40–55 MB each. They are skipped on metered connections, near your data "
                  "limit, on low battery and while you are busy downloading",
                  self._combo(AUTO_TEST_CHOICES, cfg.get("auto_test_hours"), lambda v: cfg.set("auto_test_hours", v)))
        self._add(tests, "Alert when speed drops", "Notify when an automatic test is below half your typical speed",
                  self._toggle("alert_slow_speed"))
        self.add(tests)

        # mini meter
        mini = Card("Mini meter", "A small always-on-top speed meter you can place anywhere on screen")
        self._add(mini, "Show mini meter", "Also available from the tray menu and with Ctrl+M",
                  self._toggle("mini_meter"))
        self._add(mini, "Show CPU and RAM", "Display CPU and memory usage next to network speed",
                  self._toggle("mini_meter_stats"))
        self.add(mini)

        # alerts
        alerts = Card("Alerts", "Desktop notifications when something needs your attention")
        self._add(alerts, "Enable alerts", None, self._toggle("alerts_enabled"))
        self._add(alerts, "Internet connection drops", "Notify when your internet goes down and when it's back",
                  self._toggle("alert_connection"))
        self._add(alerts, "High CPU usage", "Notify when CPU stays above this level for 30 seconds",
                  self._spin("alert_cpu", 50, 100, "%"))
        self._add(alerts, "High memory usage", "Notify when RAM usage goes above this level",
                  self._spin("alert_ram", 50, 100, "%"))
        self._add(alerts, "High CPU temperature", "Notify when the CPU gets hotter than this (°C)",
                  self._spin("alert_temp", 50, 110, " °C"))
        self.add(alerts)

        # data usage
        data = Card("Data usage")
        limit = QDoubleSpinBox()
        limit.setRange(0, 100000)
        limit.setDecimals(1)
        limit.setSuffix(" GB")
        limit.setSpecialValueText("No limit")
        limit.setValue(cfg.get("data_limit_gb"))
        limit.setMinimumWidth(140)
        limit.valueChanged.connect(lambda v: cfg.set("data_limit_gb", float(v)))
        self._add(data, "Monthly data limit", "Get warned at 80% and 100% of your plan's data cap", limit)
        day = QSpinBox()
        day.setRange(1, 28)
        day.setValue(cfg.get("billing_day"))
        day.setMinimumWidth(140)
        day.valueChanged.connect(lambda v: cfg.set("billing_day", int(v)))
        self._add(data, "Billing cycle starts on day", "Day of the month your data plan resets", day)
        reset = QPushButton("Reset")
        reset.setObjectName("Danger")
        reset.clicked.connect(self._reset_usage)
        self._add(data, "Reset usage statistics", "Delete all recorded daily data usage", reset)
        self.add(data)
        self.finish()

    # ---------------------------------------------------------------- helpers
    def _add(self, card, title, description, control):
        if card.body.count() > 1:
            card.add(divider())
        card.add(_Row(title, description, control))

    def _toggle(self, key, handler=None):
        t = Toggle(self.ctx.config.get(key))
        t.toggled.connect(handler or (lambda v, k=key: self.ctx.config.set(k, bool(v))))
        return t

    def _combo(self, items, current, on_change):
        box = QComboBox()
        box.setMinimumWidth(200)
        for value, text in items:
            box.addItem(text, value)
        idx = box.findData(current)
        box.setCurrentIndex(max(0, idx))
        box.currentIndexChanged.connect(lambda _: on_change(box.currentData()))
        return box

    def _spin(self, key, low, high, suffix):
        s = QSpinBox()
        s.setRange(low, high)
        s.setSuffix(suffix)
        s.setValue(self.ctx.config.get(key))
        s.setMinimumWidth(140)
        s.valueChanged.connect(lambda v: self.ctx.config.set(key, int(v)))
        return s

    def _set_autostart(self, enabled):
        ok = autostart.set_enabled(enabled)
        self.ctx.config.set("autostart", enabled if ok else autostart.is_enabled())
        if not ok:
            QMessageBox.warning(self, "Launch at login", "Could not update the autostart entry.")

    def _reset_usage(self):
        answer = QMessageBox.question(self, "Reset data usage",
                                      "Delete all recorded data usage history? This cannot be undone.",
                                      QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
        if answer == QMessageBox.Yes:
            self.ctx.usage.reset()
