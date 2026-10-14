"""Main application window: sidebar navigation + page stack."""

import os
import statistics
import time

from PyQt5.QtCore import QByteArray, QSize, Qt, QTimer
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QApplication, QButtonGroup, QFrame, QHBoxLayout, QMainWindow, QPushButton, QShortcut,
                             QStackedWidget, QVBoxLayout, QWidget)

from . import APP_NAME, VERSION
from . import formatting as fmt
from . import icons, system
from .alerts import AlertManager, Notifier
from .mini_meter import MiniMeter
from .monitor import Monitor
from .battery import has_battery
from .history_store import HistoryStore
from .pages.about import AboutPage
from .pages.battery import BatteryPage
from .pages.cpu import CpuPage
from .pages.disks import DisksPage
from .pages.history import HistoryPage
from .pages.memory import MemoryPage
from .pages.network import NetworkPage
from .pages.overview import OverviewPage
from .pages.processes import ProcessesPage
from .pages.settings import SettingsPage
from .pages.speedtest import SpeedTestPage
from .pages.usage import UsagePage
from .scheduler import SpeedTestScheduler
from .theme import theme
from .tray import Tray
from .usage import DataUsageStore, OutageLog, SpeedTestHistory
from .widgets.common import Dot, label

ICON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons", "speedx.png")

NAV = [
    ("MONITOR", [("overview", "Overview"), ("cpu", "CPU"), ("memory", "Memory"), ("network", "Network"),
                 ("disk", "Disks"), ("battery", "Battery"), ("processes", "Processes"), ("history", "History")]),
    ("INTERNET", [("speedtest", "Speed Test"), ("usage", "Data Usage")]),
    (None, [("settings", "Settings"), ("about", "About")]),
]


class MainWindow(QMainWindow):
    def __init__(self, config, start_hidden=False):
        super().__init__()
        self.config = config
        self.local_ip = system.local_ip()
        self.usage = DataUsageStore()
        self.outages = OutageLog()
        self.history_store = HistoryStore()
        self.has_battery = has_battery()
        self._was_online = False
        self.speed_history = SpeedTestHistory()
        self.monitor = Monitor(config.get("interval"), config.get("interface"))
        self._quitting = False

        self.app_icon = QIcon(ICON_PATH)
        self.setWindowIcon(self.app_icon)
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1000, 660)
        self.resize(1240, 820)

        self._build_tray()
        self._build_ui()
        self.notifier = Notifier(self.tray)
        self.alerts = AlertManager(config, self.usage, self.notifier)
        self.mini = MiniMeter(config)
        self.mini.open_main.connect(self.show_and_raise)
        self.mini.hide_requested.connect(lambda: config.set("mini_meter", False))
        self._build_shortcuts()
        self.scheduler = SpeedTestScheduler(self)

        self.monitor.updated.connect(self._on_snapshot)
        config.changed.connect(self._on_config_changed)
        theme.changed.connect(self._refresh_nav_icons)

        self._save_timer = QTimer(self)
        self._save_timer.timeout.connect(self.usage.save)
        self._save_timer.start(10_000)
        self._ip_timer = QTimer(self)
        self._ip_timer.timeout.connect(lambda: setattr(self, "local_ip", system.local_ip()))
        self._ip_timer.start(30_000)

        geometry = config.get("window_geometry")
        if isinstance(geometry, QByteArray):
            self.restoreGeometry(geometry)

        self.monitor.start()
        self._select_page(0)
        if config.get("mini_meter"):
            self.mini.show()

        hidden_ok = self.tray.available or config.get("mini_meter")
        if not start_hidden:
            self.show()
        elif hidden_ok:
            pass
        else:
            self.showMinimized()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        root = QWidget()
        root.setObjectName("Root")
        lay = QHBoxLayout(root)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(224)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(14, 20, 14, 16)
        side.setSpacing(2)

        brand = QHBoxLayout()
        brand.setContentsMargins(6, 0, 0, 14)
        brand.setSpacing(10)
        logo = label()
        logo.setPixmap(self.app_icon.pixmap(QSize(34, 34)))
        brand.addWidget(logo)
        names = QVBoxLayout()
        names.setSpacing(0)
        names.addWidget(label(APP_NAME, "Brand"))
        names.addWidget(label("System monitor", "BrandSub"))
        brand.addLayout(names, 1)
        side.addLayout(brand)

        self.stack = QStackedWidget()
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        self.nav_buttons = []
        self.pages = []
        page_factories = {
            "overview": lambda: OverviewPage(self),
            "cpu": lambda: CpuPage(self),
            "memory": lambda: MemoryPage(self),
            "network": lambda: NetworkPage(self),
            "disk": lambda: DisksPage(self),
            "battery": lambda: BatteryPage(self),
            "processes": lambda: ProcessesPage(self),
            "history": lambda: HistoryPage(self, self.has_battery),
            "speedtest": lambda: SpeedTestPage(self),
            "usage": lambda: UsagePage(self),
            "settings": lambda: SettingsPage(self),
            "about": lambda: AboutPage(self, ICON_PATH),
        }
        self.page_index = {}
        for section, items in NAV:
            if section:
                side.addWidget(label(section, "NavSection"))
            else:
                side.addStretch(1)
            for key, text in items:
                if key == "battery" and not self.has_battery:
                    continue
                btn = QPushButton("  " + text)
                btn.setObjectName("NavButton")
                btn.setCheckable(True)
                btn.setCursor(Qt.PointingHandCursor)
                btn.setIconSize(QSize(18, 18))
                btn.setProperty("icon_name", key)
                index = len(self.pages)
                btn.clicked.connect(lambda _, i=index: self._select_page(i))
                self.nav_group.addButton(btn, index)
                self.nav_buttons.append(btn)
                side.addWidget(btn)
                page = page_factories[key]()
                self.pages.append(page)
                self.stack.addWidget(page)
                self.page_index[key] = index

        side.addSpacing(12)
        pill = QFrame()
        pill.setObjectName("StatusPill")
        pill_lay = QVBoxLayout(pill)
        pill_lay.setContentsMargins(12, 10, 12, 10)
        pill_lay.setSpacing(4)
        top = QHBoxLayout()
        top.setSpacing(8)
        self.status_dot = Dot("faint")
        self.status_text = label("Checking connection…", "Value")
        top.addWidget(self.status_dot)
        top.addWidget(self.status_text, 1)
        pill_lay.addLayout(top)
        self.status_speed = label("", "Faint")
        pill_lay.addWidget(self.status_speed)
        side.addWidget(pill)
        side.addSpacing(6)
        side.addWidget(label(f"v{VERSION}", "Faint"), 0, Qt.AlignHCenter)

        lay.addWidget(sidebar)
        lay.addWidget(self.stack, 1)
        self.setCentralWidget(root)
        self._refresh_nav_icons()

    def _refresh_nav_icons(self):
        c = theme.colors
        for btn in self.nav_buttons:
            btn.setIcon(icons.icon(btn.property("icon_name"), c["muted"], c["accent"], 18))

    def _build_tray(self):
        self.tray = Tray(self.app_icon, self.config, self)
        self.tray.show_window.connect(self.show_and_raise)
        self.tray.toggle_mini.connect(self.toggle_mini_meter)
        self.tray.open_speedtest.connect(lambda: (self.show_and_raise(), self.go_to("speedtest")))
        self.tray.quit_requested.connect(self.quit)
        self.tray.start()

    def _build_shortcuts(self):
        for i in range(min(9, len(self.pages))):
            QShortcut(QKeySequence(f"Ctrl+{i + 1}"), self, activated=lambda i=i: self._select_page(i))
        QShortcut(QKeySequence("Ctrl+M"), self, activated=self.toggle_mini_meter)
        QShortcut(QKeySequence("Ctrl+,"), self, activated=lambda: self.go_to("settings"))
        QShortcut(QKeySequence.Quit, self, activated=self.quit)

    # ------------------------------------------------------------ behaviour
    def go_to(self, key):
        self._select_page(self.page_index[key])

    def _select_page(self, index):
        self.nav_buttons[index].setChecked(True)
        self.stack.setCurrentIndex(index)
        page = self.pages[index]
        self.monitor.set_want_processes(getattr(page, "needs_processes", False))
        page.on_shown()
        if self.monitor.last:
            page.on_snapshot(self.monitor.last, self.monitor)

    def speed(self, bytes_per_sec):
        return fmt.speed(bytes_per_sec, self.config.get("speed_unit"))

    def toggle_mini_meter(self):
        self.config.set("mini_meter", not self.config.get("mini_meter"))

    def show_and_raise(self):
        if self.isMinimized():
            self.showNormal()
        self.show()
        self.raise_()
        self.activateWindow()

    def _on_snapshot(self, snap):
        self.usage.update(snap["net_counters"], snap["boot_time"])
        self.history_store.add(snap)
        self._handle_connection_events(snap)
        self.alerts.check(snap)
        self.tray.update_stats(snap)
        self.mini.update_stats(snap)

        online = snap["online"]
        if online is None:
            self.status_dot.set_color("faint")
            self.status_text.setText("Checking…")
        elif online:
            self.status_dot.set_color("good")
            self.status_text.setText(f"Online · {snap['latency']:.0f} ms")
        else:
            self.status_dot.set_color("bad")
            since = snap.get("outage_since")
            self.status_text.setText(f"Offline · {fmt.duration_precise(time.time() - since)}" if since else "Offline")
        self.status_speed.setText(f"↓ {self.speed(snap['net_down'])}    ↑ {self.speed(snap['net_up'])}")

        if self.isVisible() and not self.isMinimized():
            self.stack.currentWidget().on_snapshot(snap, self.monitor)

    def on_speed_test_result(self, result, previous_downloads):
        """Called by the speed test page after every completed test."""
        self.scheduler.update_status()
        if not (result.get("automatic") and self.config.get("alerts_enabled") and self.config.get("alert_slow_speed")):
            return
        if len(previous_downloads) < 5:
            return
        typical = statistics.median(previous_downloads)
        if typical > 0 and result["download"] < typical * 0.5:
            self.notifier.notify("Internet slower than usual",
                                 f"Download is {result['download']:.1f} Mbps — about "
                                 f"{result['download'] / typical * 100:.0f}% of your typical {typical:.1f} Mbps.")

    def _handle_connection_events(self, snap):
        """Record finished outages and notify on connection loss / recovery."""
        notify = self.config.get("alerts_enabled") and self.config.get("alert_connection")
        for kind, start, end, reason in snap["events"]:
            if kind == "lost":
                if notify and self._was_online:
                    self.notifier.notify("Internet connection lost",
                                         f"{reason}. SpeedX will tell you when it's back.")
            elif kind == "restored":
                self.outages.add(start, end, reason)
                if notify and self._was_online:
                    self.notifier.notify("Back online",
                                         f"Your internet was down for {fmt.duration_precise(end - start)}.")
            elif kind == "closed":
                self.outages.add(start, end, reason, note="ended by sleep")
        if snap["online"]:
            self._was_online = True

    def _on_config_changed(self, key, value):
        if key == "theme":
            theme.apply(value)
        elif key == "interval":
            self.monitor.set_interval(float(value))
        elif key == "interface":
            self.monitor.set_interface(value)
        elif key == "mini_meter":
            self.tray.sync_menu()
            self.mini.setVisible(bool(value))
        elif key == "auto_test_hours":
            self.scheduler.check()
        elif key == "mini_meter_stats":
            if self.monitor.last:
                self.mini.update_stats(self.monitor.last)
        if key in ("tray_speed", "tray_content", "tray_style", "speed_unit"):
            self.tray.refresh()
        if key in ("speed_unit", "temp_unit", "interface") and self.monitor.last:
            self.stack.currentWidget().on_snapshot(self.monitor.last, self.monitor)

    # ---------------------------------------------------------------- close
    def closeEvent(self, event):
        if not self._quitting and self.config.get("close_to_tray") and self.tray.available:
            self.config.set("window_geometry", self.saveGeometry())
            event.ignore()
            self.hide()
            return
        event.accept()
        self.quit()

    def quit(self):
        if self._quitting:
            return
        self._quitting = True
        self.config.set("window_geometry", self.saveGeometry())
        self.pages[self.page_index["speedtest"]].shutdown()
        last = self.monitor.last
        if last and last.get("outage_since"):
            self.outages.add(last["outage_since"], time.time(), last.get("outage_reason") or "",
                             note="SpeedX closed")
        self.monitor.stop()
        self.usage.save()
        self.history_store.close()
        self.config.sync()
        self.tray.stop()
        self.mini.close()
        QApplication.instance().quit()
