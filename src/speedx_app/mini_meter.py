"""Small always-on-top floating speed meter."""

from PyQt5.QtCore import QPoint, QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QFontMetrics, QPainter
from PyQt5.QtWidgets import QApplication, QMenu, QWidget

from . import formatting as fmt
from . import icons
from .theme import theme


class MiniMeter(QWidget):
    open_main = pyqtSignal()
    hide_requested = pyqtSignal()

    def __init__(self, config):
        super().__init__(None, Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.config = config
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setWindowTitle("SpeedX mini meter")
        self._drag = None
        self._down = self._up = 0.0
        self._cpu = self._mem = 0.0
        theme.changed.connect(self.update)
        self._resize()
        self._restore_position()

    def _font(self, size, bold=False):
        f = QFont(self.font())
        f.setPointSizeF(size)
        f.setBold(bold)
        return f

    def _segments(self):
        unit = self.config.get("speed_unit")
        segs = [("down", "down", fmt.speed(self._down, unit)), ("up", "up", fmt.speed(self._up, unit))]
        if self.config.get("mini_meter_stats"):
            segs += [(None, "cpu", f"CPU {self._cpu:.0f}%"), (None, "mem", f"RAM {self._mem:.0f}%")]
        return segs

    def _resize(self):
        fm = QFontMetrics(self._font(9.5, True))
        width = 20
        for icon_name, _, text in self._segments():
            sample = text if icon_name is None else "000.0 MB/s"
            width += (16 if icon_name else 0) + max(fm.horizontalAdvance(sample), fm.horizontalAdvance(text)) + 18
        self.setFixedSize(width, 34)

    def _restore_position(self):
        pos = self.config.get("mini_meter_pos")
        screen = QApplication.primaryScreen().availableGeometry()
        if pos and len(pos) == 2:
            point = QPoint(int(pos[0]), int(pos[1]))
            if any(s.availableGeometry().contains(point) for s in QApplication.screens()):
                self.move(point)
                return
        self.move(screen.right() - self.width() - 24, screen.top() + 24)

    def update_stats(self, snap):
        self._down, self._up = snap["net_down"], snap["net_up"]
        self._cpu, self._mem = snap["cpu"], snap["mem"]["percent"]
        old = self.width()
        self._resize()
        if self.width() != old:
            self.move(self.x() + old - self.width(), self.y())  # keep right edge anchored
        if self.isVisible():
            self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        bg = theme.color("surface")
        bg.setAlpha(238)
        p.setPen(theme.color("border"))
        p.setBrush(bg)
        p.drawRoundedRect(rect, rect.height() / 2, rect.height() / 2)

        font = self._font(9.5, True)
        fm = QFontMetrics(font)
        p.setFont(font)
        x = 12.0
        for icon_name, color_key, text in self._segments():
            if icon_name:
                p.drawPixmap(int(x), int((self.height() - 14) / 2), icons.pixmap(icon_name, theme.colors[color_key], 14, 2.2))
                x += 16
                sample = max(fm.horizontalAdvance("000.0 MB/s"), fm.horizontalAdvance(text))
            else:
                sample = fm.horizontalAdvance(text)
            p.setPen(theme.color("text") if icon_name else theme.color(color_key))
            p.drawText(QRectF(x, 0, sample, self.height()), Qt.AlignLeft | Qt.AlignVCenter, text)
            x += sample + 18

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag)

    def mouseReleaseEvent(self, event):
        if self._drag is not None:
            self._drag = None
            self.config.set("mini_meter_pos", [self.x(), self.y()])

    def mouseDoubleClickEvent(self, event):
        self.open_main.emit()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.addAction("Open SpeedX", self.open_main.emit)
        stats = menu.addAction("Show CPU and RAM")
        stats.setCheckable(True)
        stats.setChecked(self.config.get("mini_meter_stats"))
        stats.toggled.connect(lambda v: self.config.set("mini_meter_stats", v))
        tray = menu.addAction("Show speed in system tray")
        tray.setCheckable(True)
        tray.setChecked(self.config.get("tray_speed"))
        tray.toggled.connect(lambda v: self.config.set("tray_speed", v))
        menu.addSeparator()
        menu.addAction("Hide mini meter", self.hide_requested.emit)
        menu.exec_(event.globalPos())
