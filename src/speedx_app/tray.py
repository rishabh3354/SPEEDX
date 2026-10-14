"""System tray integration with live speed.

Two backends:
  * "sni": our own StatusNotifierItem (see sni.py). Supports a text label next to
    the icon, shown by Ubuntu GNOME's AppIndicator extension, XFCE, MATE, Budgie.
  * "qt":  QSystemTrayIcon fallback for other trays. No label support, so the
    speed is drawn inside the icon instead.
"""

import os

from PyQt5.QtCore import QObject, QRectF, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QIcon, QImage, QPainter, QPixmap
from PyQt5.QtWidgets import QMenu, QSystemTrayIcon

from . import APP_ID, APP_NAME
from . import formatting as fmt

try:
    from .sni import MenuItem, StatusNotifierItem, image_to_pixmap
except ImportError:  # jeepney not installed
    StatusNotifierItem = None

DOWN_COLOR = "#14b8a6"
UP_COLOR = "#ec4899"
ICON_SIZES = (16, 22, 24, 32, 48, 64)
CONTENT_CHOICES = [
    ("both", "Download and upload"),
    ("down", "Download only"),
    ("total", "Combined speed"),
    ("all", "Speed, CPU and RAM"),
]


def _label_segment(arrow, bytes_per_sec, unit):
    text = fmt.speed_fixed(bytes_per_sec, unit)
    number = text.lstrip(fmt.FIGURE_SPACE)
    pad = text[:len(text) - len(number)]
    return f"{pad}{arrow} {number}"


def speed_label(snap, content, unit):
    down, up = snap["net_down"], snap["net_up"]
    if content == "down":
        return _label_segment("↓", down, unit)
    if content == "total":
        return _label_segment("⇅", down + up, unit)
    text = _label_segment("↓", down, unit) + "  " + _label_segment("↑", up, unit)
    if content == "all":
        cpu = f"{snap['cpu']:.0f}%".rjust(4, fmt.FIGURE_SPACE)
        ram = f"{snap['mem']['percent']:.0f}%".rjust(4, fmt.FIGURE_SPACE)
        text += f"   CPU{cpu}  RAM{ram}"
    return text


def render_speed_icon(lines, size=64):
    """Draw one or two (text, color) lines filling a square image."""
    img = QImage(size, size, QImage.Format_ARGB32)
    img.fill(Qt.transparent)
    p = QPainter(img)
    p.setRenderHint(QPainter.Antialiasing)
    p.setRenderHint(QPainter.TextAntialiasing)
    font = QFont()
    font.setBold(True)
    rows = len(lines)
    pixel = int(size / rows * 0.92)
    widest = max(lines, key=lambda line: len(line[0]))[0]
    while pixel > 6:
        font.setPixelSize(pixel)
        if QFontMetrics(font).horizontalAdvance(widest) <= size:
            break
        pixel -= 1
    p.setFont(font)
    for i, (text, color) in enumerate(lines):
        p.setPen(QColor(color))
        p.drawText(QRectF(0, i * size / rows, size, size / rows), Qt.AlignCenter, text)
    p.end()
    return img


class Tray(QObject):
    show_window = pyqtSignal()
    toggle_mini = pyqtSignal()
    open_speedtest = pyqtSignal()
    quit_requested = pyqtSignal()
    _menu_action = pyqtSignal(str)  # emitted from the D-Bus thread

    def __init__(self, icon, config, parent=None):
        super().__init__(parent)
        self.icon = icon
        self.config = config
        self.backend = None
        self._sni = None
        self._qt = None
        self._last_icon_key = None
        self._last_snap = None
        self._menu_action.connect(self._on_menu_action)

    # -------------------------------------------------------------- startup
    def start(self):
        if StatusNotifierItem is not None and os.environ.get("SPEEDX_TRAY") != "qt" \
                and StatusNotifierItem.watcher_available():
            try:
                self.backend = "sni"
                self._start_sni()
                return
            except Exception:  # noqa: BLE001 - fall back to Qt's tray
                self._sni = None
                self.backend = None
        if QSystemTrayIcon.isSystemTrayAvailable():
            self._start_qt()
            self.backend = "qt"

    def _start_sni(self):
        sni = StatusNotifierItem(APP_ID, APP_NAME, on_activate=lambda: self._menu_action.emit("open"))
        sni.set_icon(self._logo_pixmaps())
        sni.menu_items = self._sni_menu()
        sni.start()
        self._sni = sni

    def _start_qt(self):
        tray = QSystemTrayIcon(self.icon, self)
        menu = QMenu()
        menu.addAction("Open SpeedX", self.show_window.emit)
        menu.addAction("Run speed test", self.open_speedtest.emit)
        menu.addSeparator()
        self._qt_speed = menu.addAction("Show speed in tray", lambda: self._on_menu_action("speed"))
        self._qt_speed.setCheckable(True)
        self._qt_mini = menu.addAction("Mini meter", self.toggle_mini.emit)
        self._qt_mini.setCheckable(True)
        menu.addSeparator()
        menu.addAction("Quit", self.quit_requested.emit)
        self._qt_menu = menu
        tray.setContextMenu(menu)
        tray.activated.connect(lambda reason: self.show_window.emit()
                               if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick) else None)
        tray.setToolTip(APP_NAME)
        tray.show()
        self._qt = tray
        self.sync_menu()

    def stop(self):
        if self._sni:
            self._sni.stop()
            self._sni = None
        if self._qt:
            self._qt.hide()

    # ----------------------------------------------------------- properties
    @property
    def available(self):
        return self.backend is not None

    @property
    def supports_label(self):
        return self.backend == "sni"

    def label_mode(self):
        """True when speed is shown as text beside the icon, False when drawn in the icon."""
        if not self.supports_label:
            return False
        style = self.config.get("tray_style")
        if style == "auto":
            desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").upper()
            return not any(d in desktop for d in ("KDE", "LXQT"))
        return style == "label"

    # ----------------------------------------------------------------- menu
    def _sni_menu(self):
        cfg = self.config
        emit = self._menu_action.emit
        return [
            MenuItem("Open SpeedX", lambda: emit("open")),
            MenuItem("Run speed test", lambda: emit("speedtest")),
            MenuItem(separator=True),
            MenuItem("Show speed in top bar" if self.label_mode() else "Show speed in tray", lambda: emit("speed"),
                     checkable=True, checked=cfg.get("tray_speed")),
            MenuItem("Mini meter", lambda: emit("mini"), checkable=True, checked=cfg.get("mini_meter")),
            MenuItem(separator=True),
            MenuItem("Quit", lambda: emit("quit")),
        ]

    def sync_menu(self):
        if self._sni:
            self._sni.set_menu(self._sni_menu())
        if self._qt:
            self._qt_speed.setChecked(self.config.get("tray_speed"))
            self._qt_mini.setChecked(self.config.get("mini_meter"))

    def _on_menu_action(self, action):
        if action == "open":
            self.show_window.emit()
        elif action == "speedtest":
            self.open_speedtest.emit()
        elif action == "speed":
            self.config.set("tray_speed", not self.config.get("tray_speed"))
        elif action == "mini":
            self.toggle_mini.emit()
        elif action == "quit":
            self.quit_requested.emit()

    # ---------------------------------------------------------------- icons
    def _logo_pixmaps(self):
        return [image_to_pixmap(self.icon.pixmap(QSize(s, s)).toImage().scaled(
            s, s, Qt.KeepAspectRatio, Qt.SmoothTransformation)) for s in ICON_SIZES]

    def _speed_lines(self, snap):
        unit = self.config.get("speed_unit")
        down, up = snap["net_down"], snap["net_up"]
        content = self.config.get("tray_content")
        if content == "down":
            return [(fmt.speed_compact(down, unit), DOWN_COLOR)]
        if content == "total":
            return [(fmt.speed_compact(down + up, unit), DOWN_COLOR)]
        return [(fmt.speed_compact(down, unit), DOWN_COLOR), (fmt.speed_compact(up, unit), UP_COLOR)]

    def _apply_icon(self, lines):
        key = tuple(lines) if lines else "logo"
        if key == self._last_icon_key:
            return
        self._last_icon_key = key
        if self._sni:
            if lines:
                self._sni.set_icon([image_to_pixmap(render_speed_icon(lines, s)) for s in (22, 32, 48, 64)])
            else:
                self._sni.set_icon(self._logo_pixmaps())
        if self._qt:
            self._qt.setIcon(QIcon(QPixmap.fromImage(render_speed_icon(lines, 64))) if lines else self.icon)

    # ---------------------------------------------------------------- stats
    def refresh(self):
        self._last_icon_key = None
        self.sync_menu()
        if self._last_snap:
            self.update_stats(self._last_snap)
        elif self._sni:
            self._sni.set_label("")

    def update_stats(self, snap):
        self._last_snap = snap
        if not self.available:
            return
        unit = self.config.get("speed_unit")
        down, up = fmt.speed(snap["net_down"], unit), fmt.speed(snap["net_up"], unit)
        body = f"↓ {down}   ↑ {up}\nCPU {snap['cpu']:.0f}%   RAM {snap['mem']['percent']:.0f}%"

        show_speed = self.config.get("tray_speed")
        label_mode = self.label_mode()
        if self._sni:
            if show_speed and label_mode:
                content = self.config.get("tray_content")
                self._sni.set_label(speed_label(snap, content, unit),
                                    speed_label({"net_down": 999e6, "net_up": 999e6, "cpu": 100,
                                                 "mem": {"percent": 100}}, content, unit))
            else:
                self._sni.set_label("")
            self._sni.set_tooltip(APP_NAME, body)
        if self._qt:
            self._qt.setToolTip(f"{APP_NAME}\n{body}")
        self._apply_icon(self._speed_lines(snap) if show_speed and not label_mode else None)

    def show_message(self, title, message):
        if self._qt and self._qt.isVisible():
            self._qt.showMessage(title, message, QSystemTrayIcon.Information, 8000)
            return True
        return False
