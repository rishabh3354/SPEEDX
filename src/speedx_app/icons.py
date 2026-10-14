"""Line icons drawn with QPainter, so they follow the theme colors."""

import math

from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen, QPixmap


def _overview(p):
    for x, y in ((3, 3), (13, 3), (3, 13), (13, 13)):
        p.drawRoundedRect(QRectF(x, y, 8, 8), 2, 2)


def _cpu(p):
    p.drawRoundedRect(QRectF(6, 6, 12, 12), 2, 2)
    p.drawRect(QRectF(9.5, 9.5, 5, 5))
    for v in (9, 12, 15):
        p.drawLine(QPointF(v, 2.5), QPointF(v, 6))
        p.drawLine(QPointF(v, 18), QPointF(v, 21.5))
        p.drawLine(QPointF(2.5, v), QPointF(6, v))
        p.drawLine(QPointF(18, v), QPointF(21.5, v))


def _memory(p):
    p.drawRoundedRect(QRectF(2.5, 6, 19, 10), 2, 2)
    for x in (6.5, 10.5, 14.5):
        p.drawRect(QRectF(x, 9, 2.5, 4))
    for x in (5, 9, 13, 17):
        p.drawLine(QPointF(x + 1, 16), QPointF(x + 1, 19))


def _network(p):
    p.drawLine(QPointF(8, 4), QPointF(8, 20))
    p.drawLine(QPointF(4, 16), QPointF(8, 20))
    p.drawLine(QPointF(12, 16), QPointF(8, 20))
    p.drawLine(QPointF(16, 20), QPointF(16, 4))
    p.drawLine(QPointF(12, 8), QPointF(16, 4))
    p.drawLine(QPointF(20, 8), QPointF(16, 4))


def _speedtest(p):
    p.drawArc(QRectF(3, 5, 18, 18), 0, 180 * 16)
    p.drawLine(QPointF(3, 14), QPointF(21, 14))
    p.drawLine(QPointF(12, 14), QPointF(16.5, 8.5))
    p.drawEllipse(QPointF(12, 14), 1.2, 1.2)


def _usage(p):
    p.drawLine(QPointF(3, 20.5), QPointF(21, 20.5))
    p.drawRoundedRect(QRectF(5, 11, 3.5, 7), 1, 1)
    p.drawRoundedRect(QRectF(10.25, 5, 3.5, 13), 1, 1)
    p.drawRoundedRect(QRectF(15.5, 8, 3.5, 10), 1, 1)


def _disk(p):
    p.drawEllipse(QRectF(4, 3, 16, 5.5))
    p.drawLine(QPointF(4, 5.75), QPointF(4, 18.25))
    p.drawLine(QPointF(20, 5.75), QPointF(20, 18.25))
    p.drawArc(QRectF(4, 15.5, 16, 5.5), 180 * 16, 180 * 16)
    p.drawArc(QRectF(4, 9.5, 16, 5.5), 180 * 16, 180 * 16)


def _processes(p):
    for y in (6, 12, 18):
        p.drawEllipse(QPointF(5, y), 1.2, 1.2)
        p.drawLine(QPointF(9, y), QPointF(20, y))


def _settings(p):
    p.drawEllipse(QPointF(12, 12), 3, 3)
    path = QPainterPath()
    teeth = 8
    for i in range(teeth * 2):
        a0 = (i / (teeth * 2)) * 2 * math.pi
        a1 = ((i + 1) / (teeth * 2)) * 2 * math.pi
        r = 9 if i % 2 == 0 else 7
        pt0 = QPointF(12 + r * math.cos(a0), 12 + r * math.sin(a0))
        pt1 = QPointF(12 + r * math.cos(a1), 12 + r * math.sin(a1))
        if i == 0:
            path.moveTo(pt0)
        else:
            path.lineTo(pt0)
        path.lineTo(pt1)
    path.closeSubpath()
    p.drawPath(path)


def _about(p):
    p.drawEllipse(QPointF(12, 12), 9, 9)
    p.drawLine(QPointF(12, 11), QPointF(12, 16.5))
    p.drawPoint(QPointF(12, 7.8))


def _down(p):
    p.drawLine(QPointF(12, 4), QPointF(12, 20))
    p.drawLine(QPointF(6, 14), QPointF(12, 20))
    p.drawLine(QPointF(18, 14), QPointF(12, 20))


def _up(p):
    p.drawLine(QPointF(12, 20), QPointF(12, 4))
    p.drawLine(QPointF(6, 10), QPointF(12, 4))
    p.drawLine(QPointF(18, 10), QPointF(12, 4))


def _ping(p):
    path = QPainterPath(QPointF(2, 12))
    for x, y in ((7, 12), (9.5, 6), (13, 18), (15.5, 12), (22, 12)):
        path.lineTo(QPointF(x, y))
    p.drawPath(path)


def _temp(p):
    p.drawRoundedRect(QRectF(9.5, 2.5, 5, 13), 2.5, 2.5)
    p.drawEllipse(QPointF(12, 17.5), 4, 4)
    p.drawLine(QPointF(12, 8), QPointF(12, 15))


def _mini(p):
    p.drawRoundedRect(QRectF(2.5, 7, 19, 10), 5, 5)
    p.drawLine(QPointF(7, 10.5), QPointF(7, 13.5))
    p.drawLine(QPointF(17, 10.5), QPointF(17, 13.5))


def _refresh(p):
    p.drawArc(QRectF(4, 4, 16, 16), 30 * 16, 290 * 16)
    p.drawLine(QPointF(19.5, 3.5), QPointF(19.5, 8.5))
    p.drawLine(QPointF(19.5, 8.5), QPointF(14.5, 8.5))


def _history(p):
    p.drawArc(QRectF(3.5, 3.5, 17, 17), 200 * 16, -310 * 16)
    p.drawLine(QPointF(3.2, 8.5), QPointF(4.2, 12.6))
    p.drawLine(QPointF(4.2, 12.6), QPointF(8.2, 11.4))
    p.drawLine(QPointF(12, 7.5), QPointF(12, 12))
    p.drawLine(QPointF(12, 12), QPointF(15, 14))


def _battery(p):
    p.drawRoundedRect(QRectF(2.5, 7, 17, 10), 2, 2)
    p.drawLine(QPointF(21.5, 10.5), QPointF(21.5, 13.5))
    p.setBrush(p.pen().color())
    p.drawRect(QRectF(5, 9.5, 8, 5))
    p.setBrush(Qt.NoBrush)


def _download_file(p):
    p.drawLine(QPointF(12, 3.5), QPointF(12, 15))
    p.drawLine(QPointF(7.5, 10.5), QPointF(12, 15))
    p.drawLine(QPointF(16.5, 10.5), QPointF(12, 15))
    p.drawLine(QPointF(4, 19.5), QPointF(20, 19.5))


_DRAW = {
    "overview": _overview, "cpu": _cpu, "memory": _memory, "network": _network,
    "speedtest": _speedtest, "usage": _usage, "disk": _disk, "processes": _processes,
    "settings": _settings, "about": _about, "down": _down, "up": _up, "ping": _ping,
    "temp": _temp, "mini": _mini, "refresh": _refresh, "history": _history, "battery": _battery,
    "export": _download_file,
}


def pixmap(name, color, size=20, width=1.8, ratio=2.0):
    pm = QPixmap(int(size * ratio), int(size * ratio))
    pm.fill(Qt.transparent)
    pm.setDevicePixelRatio(ratio)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    p.scale(size / 24.0, size / 24.0)
    pen = QPen(QColor(color), width * 24.0 / size * (size / 20.0))
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.NoBrush)
    _DRAW[name](p)
    p.end()
    return pm


def icon(name, color, active_color=None, size=20):
    ic = QIcon()
    ic.addPixmap(pixmap(name, color, size), QIcon.Normal, QIcon.Off)
    if active_color:
        ic.addPixmap(pixmap(name, active_color, size), QIcon.Normal, QIcon.On)
        ic.addPixmap(pixmap(name, active_color, size), QIcon.Active, QIcon.Off)
    return ic
