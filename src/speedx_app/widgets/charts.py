"""Custom painted charts and gauges."""

import datetime as _dt
import math
import time as _time

from PyQt5.QtCore import QPointF, QRectF, QSize, Qt
from PyQt5.QtGui import QFont, QFontMetrics, QLinearGradient, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QSizePolicy, QWidget

from ..theme import theme


def nice_ceiling(value):
    if value <= 0:
        return 1.0
    exp = 10 ** math.floor(math.log10(value))
    for m in (1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if value <= m * exp:
            return m * exp
    return 10 * exp


class _Themed(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        theme.changed.connect(self.update)

    def _font(self, point_size, weight=QFont.Normal):
        f = QFont(self.font())
        f.setPointSizeF(point_size)
        f.setWeight(weight)
        return f


class LineChart(_Themed):
    """Rolling time series chart with optional grid, axis labels and hover readout.

    series: list of (label, color key) tuples.
    """

    def __init__(self, series, capacity=120, y_max=None, min_y_max=1.0, formatter=None,
                 axes=True, fill=True, line_width=2.0, parent=None):
        super().__init__(parent)
        self.series = series
        self.capacity = capacity
        self.fixed_max = y_max
        self.min_y_max = min_y_max
        self.formatter = formatter or (lambda v: f"{v:.0f}%")
        self.axes = axes
        self.fill = fill
        self.line_width = line_width
        self.data = [[] for _ in series]
        self._hover_x = None
        self.setMouseTracking(axes)
        self.setMinimumHeight(60 if not axes else 140)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_data(self, *sequences, capacity=None):
        if capacity:
            self.capacity = capacity
        self.data = [list(seq) for seq in sequences]
        if self.isVisible():
            self.update()

    def set_formatter(self, formatter):
        self.formatter = formatter
        self.update()

    def leaveEvent(self, event):
        self._hover_x = None
        self.update()

    def mouseMoveEvent(self, event):
        self._hover_x = event.pos().x()
        self.update()

    def _y_max(self):
        if self.fixed_max is not None:
            return self.fixed_max
        peak = max((max(d) for d in self.data if d), default=0)
        return nice_ceiling(max(peak * 1.1, self.min_y_max))

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        label_font = self._font(8)
        fm = QFontMetrics(label_font)
        y_max = self._y_max()

        right_pad = (fm.horizontalAdvance(self.formatter(y_max)) + 12) if self.axes else 0
        top_pad = fm.height() / 2 + 2 if self.axes else 3
        plot = QRectF(0, top_pad, self.width() - right_pad, self.height() - top_pad - (fm.height() / 2 + 2 if self.axes else 3))
        if plot.width() <= 10 or plot.height() <= 10:
            return

        if self.axes:
            p.setFont(label_font)
            grid_pen = QPen(theme.color("grid"), 1)
            grid_pen.setStyle(Qt.DashLine)
            for i in range(5):
                y = plot.top() + plot.height() * i / 4
                p.setPen(grid_pen)
                p.drawLine(QPointF(plot.left(), y), QPointF(plot.right(), y))
                p.setPen(theme.color("faint"))
                p.drawText(QRectF(plot.right() + 8, y - fm.height() / 2, right_pad, fm.height()),
                           Qt.AlignLeft | Qt.AlignVCenter, self.formatter(y_max * (4 - i) / 4))

        step = plot.width() / max(self.capacity - 1, 1)

        def point(idx, n, value):
            x = plot.right() - (n - 1 - idx) * step
            y = plot.bottom() - min(max(value, 0) / y_max, 1.0) * plot.height()
            return QPointF(x, y)

        p.setClipRect(plot.adjusted(-1, -2, 1, 1))
        for (label, color_key), values in zip(self.series, self.data):
            values = values[-self.capacity:]
            n = len(values)
            if n < 2:
                continue
            color = theme.color(color_key)
            path = QPainterPath(point(0, n, values[0]))
            for i in range(1, n):
                path.lineTo(point(i, n, values[i]))
            if self.fill:
                area = QPainterPath(path)
                area.lineTo(QPointF(plot.right(), plot.bottom()))
                area.lineTo(QPointF(point(0, n, 0).x(), plot.bottom()))
                area.closeSubpath()
                grad = QLinearGradient(0, plot.top(), 0, plot.bottom())
                grad.setColorAt(0, theme.color(color_key, 90 if theme.is_dark else 70))
                grad.setColorAt(1, theme.color(color_key, 0))
                p.fillPath(area, grad)
            pen = QPen(color, self.line_width)
            pen.setJoinStyle(Qt.RoundJoin)
            p.setPen(pen)
            p.drawPath(path)
        p.setClipping(False)

        if self.axes and self._hover_x is not None and plot.left() <= self._hover_x <= plot.right():
            self._draw_hover(p, plot, step, y_max, label_font, fm)

    def _draw_hover(self, p, plot, step, y_max, font, fm):
        offset = round((plot.right() - self._hover_x) / step)
        x = plot.right() - offset * step
        lines = []
        for (label, color_key), values in zip(self.series, self.data):
            if offset < len(values):
                v = values[len(values) - 1 - offset]
                lines.append((color_key, f"{label}  {self.formatter(v)}" if label else self.formatter(v)))
                y = plot.bottom() - min(max(v, 0) / y_max, 1.0) * plot.height()
                p.setPen(QPen(theme.color("surface"), 2))
                p.setBrush(theme.color(color_key))
                p.drawEllipse(QPointF(x, y), 4, 4)
        if not lines:
            return
        p.setPen(QPen(theme.color("faint"), 1, Qt.DotLine))
        p.drawLine(QPointF(x, plot.top()), QPointF(x, plot.bottom()))
        lines.insert(0, ("muted", f"{offset}s ago" if offset else "now"))
        width = max(fm.horizontalAdvance(t) for _, t in lines) + 30
        height = len(lines) * (fm.height() + 2) + 12
        bx = x + 12 if x + 12 + width < plot.right() else x - 12 - width
        box = QRectF(bx, plot.top() + 4, width, height)
        p.setPen(QPen(theme.color("border"), 1))
        p.setBrush(theme.color("surface2"))
        p.drawRoundedRect(box, 8, 8)
        p.setFont(font)
        for i, (color_key, text) in enumerate(lines):
            ty = box.top() + 6 + i * (fm.height() + 2)
            if i:
                p.setPen(Qt.NoPen)
                p.setBrush(theme.color(color_key))
                p.drawEllipse(QPointF(box.left() + 12, ty + fm.height() / 2), 3.5, 3.5)
            p.setPen(theme.color("text" if i else "muted"))
            p.drawText(QRectF(box.left() + 22 if i else box.left() + 10, ty, width, fm.height()),
                       Qt.AlignLeft | Qt.AlignVCenter, text)


class Sparkline(LineChart):
    def __init__(self, color_key, capacity=60, y_max=None, min_y_max=1.0, parent=None):
        super().__init__([("", color_key)], capacity=capacity, y_max=y_max, min_y_max=min_y_max,
                         axes=False, fill=True, line_width=1.6, parent=parent)
        self.setMinimumHeight(44)

    def set_color(self, color_key):
        self.series = [("", color_key)]
        self.update()


class RingGauge(_Themed):
    def __init__(self, color_key="accent", thickness=12, parent=None):
        super().__init__(parent)
        self.color_key = color_key
        self.thickness = thickness
        self.value = 0.0
        self.text = "0%"
        self.subtext = ""
        self.setMinimumSize(140, 140)

    def sizeHint(self):
        return QSize(170, 170)

    def set_value(self, percent, text=None, subtext=None):
        self.value = max(0.0, min(100.0, percent))
        self.text = text if text is not None else f"{percent:.0f}%"
        if subtext is not None:
            self.subtext = subtext
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        side = min(self.width(), self.height()) - self.thickness - 4
        rect = QRectF((self.width() - side) / 2, (self.height() - side) / 2, side, side)
        pen = QPen(theme.color("surface2"), self.thickness, Qt.SolidLine, Qt.RoundCap)
        p.setPen(pen)
        p.drawArc(rect, 0, 360 * 16)
        if self.value > 0:
            pen.setColor(theme.color(self.color_key))
            p.setPen(pen)
            p.drawArc(rect, 90 * 16, int(-self.value / 100 * 360 * 16))
        p.setPen(theme.color("text"))
        p.setFont(self._font(max(12, side / 7.5), QFont.Bold))
        if self.subtext:
            p.drawText(rect.adjusted(0, -side * 0.12, 0, -side * 0.12), Qt.AlignCenter, self.text)
            p.setPen(theme.color("muted"))
            p.setFont(self._font(max(8, side / 16)))
            p.drawText(rect.adjusted(0, side * 0.2, 0, side * 0.2), Qt.AlignCenter, self.subtext)
        else:
            p.drawText(rect, Qt.AlignCenter, self.text)


class SpeedGauge(_Themed):
    """270° speedometer with a non linear Mbps scale."""

    MARKS = [0, 5, 10, 25, 50, 100, 250, 500, 1000]
    START, SPAN = 225.0, -270.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0.0
        self.color_key = "accent"
        self.caption = "Ready"
        self.number = "0"
        self.unit = "Mbps"
        self.setMinimumSize(300, 280)

    def set_state(self, value, color_key=None, caption=None, number=None, unit="Mbps"):
        self.value = max(0.0, value)
        if color_key:
            self.color_key = color_key
        if caption is not None:
            self.caption = caption
        self.number = number if number is not None else (f"{value:.1f}" if value < 100 else f"{value:.0f}")
        self.unit = unit
        self.update()

    def _fraction(self, value):
        marks = self.MARKS
        if value >= marks[-1]:
            return 1.0
        for i in range(len(marks) - 1):
            if value <= marks[i + 1]:
                local = (value - marks[i]) / (marks[i + 1] - marks[i])
                return (i + local) / (len(marks) - 1)
        return 1.0

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        side = min(self.width(), self.height() * 1.08) - 40
        thick = max(10.0, side / 17)
        rect = QRectF((self.width() - side) / 2, (self.height() - side) / 2 + side * 0.06, side, side)
        center = rect.center()

        pen = QPen(theme.color("surface2"), thick, Qt.SolidLine, Qt.RoundCap)
        p.setPen(pen)
        p.drawArc(rect, int(self.START * 16), int(self.SPAN * 16))

        frac = self._fraction(self.value)
        if frac > 0.001:
            grad_pen = QPen(theme.color(self.color_key), thick, Qt.SolidLine, Qt.RoundCap)
            p.setPen(grad_pen)
            p.drawArc(rect, int(self.START * 16), int(self.SPAN * frac * 16))

        # scale labels
        p.setFont(self._font(max(7.5, side / 40)))
        p.setPen(theme.color("faint"))
        label_r = side / 2 - thick - side * 0.07
        for i, mark in enumerate(self.MARKS):
            angle = math.radians(self.START + self.SPAN * i / (len(self.MARKS) - 1))
            x = center.x() + label_r * math.cos(angle)
            y = center.y() - label_r * math.sin(angle)
            p.drawText(QRectF(x - 22, y - 9, 44, 18), Qt.AlignCenter, str(mark))

        # needle dot at value
        angle = math.radians(self.START + self.SPAN * frac)
        r = side / 2
        dot = QPointF(center.x() + r * math.cos(angle), center.y() - r * math.sin(angle))
        p.setPen(QPen(theme.color("surface"), 3))
        p.setBrush(theme.color("text"))
        p.drawEllipse(dot, thick * 0.42, thick * 0.42)

        p.setPen(theme.color("text"))
        p.setFont(self._font(max(20, side / 6.5), QFont.Bold))
        p.drawText(QRectF(rect.left(), center.y() - side * 0.17, side, side * 0.22), Qt.AlignCenter, self.number)
        p.setPen(theme.color("muted"))
        p.setFont(self._font(max(9, side / 26), QFont.DemiBold))
        p.drawText(QRectF(rect.left(), center.y() + side * 0.06, side, side * 0.08), Qt.AlignCenter, self.unit)
        p.setPen(theme.color(self.color_key))
        p.setFont(self._font(max(9, side / 28), QFont.DemiBold))
        p.drawText(QRectF(rect.left(), center.y() + side * 0.27, side, side * 0.1), Qt.AlignCenter, self.caption)


class BarChart(_Themed):
    """Stacked bars, one per category, with hover readout.

    bars: list of (label, [value per series]); series: list of (name, color key).
    """

    def __init__(self, series, formatter, parent=None):
        super().__init__(parent)
        self.series = series
        self.formatter = formatter
        self.bars = []
        self._hover = None
        self.setMouseTracking(True)
        self.setMinimumHeight(200)

    def set_bars(self, bars):
        self.bars = bars
        self.update()

    def leaveEvent(self, event):
        self._hover = None
        self.update()

    def mouseMoveEvent(self, event):
        if not self.bars:
            return
        plot = self._plot_rect()
        slot = plot.width() / len(self.bars)
        idx = int((event.pos().x() - plot.left()) // slot)
        self._hover = idx if 0 <= idx < len(self.bars) else None
        self.update()

    def _plot_rect(self):
        fm = QFontMetrics(self._font(8))
        y_max = self._y_max()
        right = fm.horizontalAdvance(self.formatter(y_max)) + 12
        return QRectF(0, fm.height() / 2 + 2, self.width() - right, self.height() - fm.height() * 2 - 8)

    def _y_max(self):
        peak = max((sum(v) for _, v in self.bars), default=0)
        return nice_ceiling(max(peak * 1.1, 1e6))

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        font = self._font(8)
        fm = QFontMetrics(font)
        p.setFont(font)
        plot = self._plot_rect()
        y_max = self._y_max()

        grid_pen = QPen(theme.color("grid"), 1, Qt.DashLine)
        for i in range(5):
            y = plot.top() + plot.height() * i / 4
            p.setPen(grid_pen)
            p.drawLine(QPointF(plot.left(), y), QPointF(plot.right(), y))
            p.setPen(theme.color("faint"))
            p.drawText(QRectF(plot.right() + 8, y - fm.height() / 2, 80, fm.height()),
                       Qt.AlignLeft | Qt.AlignVCenter, self.formatter(y_max * (4 - i) / 4))
        if not self.bars:
            return

        slot = plot.width() / len(self.bars)
        bar_w = max(3.0, min(28.0, slot * 0.62))
        label_every = max(1, math.ceil(len(self.bars) / max(1, plot.width() / 46)))
        for i, (label, values) in enumerate(self.bars):
            x = plot.left() + slot * i + (slot - bar_w) / 2
            bottom = plot.bottom()
            if i == self._hover:
                p.setPen(Qt.NoPen)
                p.setBrush(theme.color("hover"))
                p.drawRoundedRect(QRectF(plot.left() + slot * i, plot.top(), slot, plot.height()), 6, 6)
            for (name, color_key), v in zip(self.series, values):
                h = v / y_max * plot.height()
                if h <= 0:
                    continue
                p.setPen(Qt.NoPen)
                p.setBrush(theme.color(color_key))
                p.drawRoundedRect(QRectF(x, bottom - h, bar_w, max(h, 1.5)), 2, 2)
                bottom -= h
            if (len(self.bars) - 1 - i) % label_every == 0:
                p.setPen(theme.color("faint"))
                p.drawText(QRectF(plot.left() + slot * i - 20, plot.bottom() + 6, slot + 40, fm.height()),
                           Qt.AlignHCenter | Qt.AlignTop, label)

        if self._hover is not None:
            label, values = self.bars[self._hover]
            lines = [("muted", label)] + [(ck, f"{n}  {self.formatter(v)}") for (n, ck), v in zip(self.series, values)]
            lines.append(("text", f"Total  {self.formatter(sum(values))}"))
            width = max(fm.horizontalAdvance(t) for _, t in lines) + 34
            height = len(lines) * (fm.height() + 2) + 12
            cx = plot.left() + slot * (self._hover + 0.5)
            bx = cx + 14 if cx + 14 + width < plot.right() else cx - 14 - width
            box = QRectF(bx, plot.top() + 4, width, height)
            p.setPen(QPen(theme.color("border"), 1))
            p.setBrush(theme.color("surface2"))
            p.drawRoundedRect(box, 8, 8)
            for i, (ck, text) in enumerate(lines):
                ty = box.top() + 6 + i * (fm.height() + 2)
                indent = 10
                if 0 < i < len(lines) - 1:
                    p.setPen(Qt.NoPen)
                    p.setBrush(theme.color(ck))
                    p.drawEllipse(QPointF(box.left() + 13, ty + fm.height() / 2), 3.5, 3.5)
                    indent = 23
                p.setPen(theme.color("muted" if i == 0 else "text"))
                p.drawText(QRectF(box.left() + indent, ty, width, fm.height()), Qt.AlignLeft | Qt.AlignVCenter, text)


class MeterBar(_Themed):
    """Thin rounded horizontal progress bar."""

    def __init__(self, color_key="accent", height=8, parent=None):
        super().__init__(parent)
        self.color_key = color_key
        self.fraction = 0.0
        self.setFixedHeight(height)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def set_fraction(self, fraction, color_key=None):
        self.fraction = max(0.0, min(1.0, fraction))
        if color_key:
            self.color_key = color_key
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = self.height() / 2
        p.setPen(Qt.NoPen)
        p.setBrush(theme.color("surface2"))
        p.drawRoundedRect(QRectF(self.rect()), r, r)
        if self.fraction > 0:
            w = max(self.height(), self.width() * self.fraction)
            p.setBrush(theme.color(self.color_key))
            p.drawRoundedRect(QRectF(0, 0, w, self.height()), r, r)


_TICKS = [(600, "%H:%M"), (1800, "%H:%M"), (3600, "%H:%M"), (3 * 3600, "%H:%M"), (6 * 3600, "%H:%M"),
          (86400, "%a %d"), (2 * 86400, "%d %b"), (5 * 86400, "%d %b"), (7 * 86400, "%d %b"),
          (14 * 86400, "%d %b"), (30 * 86400, "%b %Y")]


class TimeSeriesChart(_Themed):
    """Chart over real time with gaps, optional shaded bands and point markers.

    series: list of (label, color key). Data per series: list of (epoch seconds, value or None).
    """

    def __init__(self, series, formatter=None, y_max=None, min_y_max=1.0, markers=False, parent=None):
        super().__init__(parent)
        self.series = series
        self.formatter = formatter or (lambda v: f"{v:.0f}%")
        self.fixed_max = y_max
        self.min_y_max = min_y_max
        self.markers = markers
        self.data = [[] for _ in series]
        self.start = self.end = 0
        self.step = 60
        self.bands = []
        self.empty_text = "No data yet for this period"
        self._hover_x = None
        self.setMouseTracking(True)
        self.setMinimumHeight(170)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_data(self, data, start, end, step, bands=()):
        self.data = [list(d) for d in data]
        self.start, self.end, self.step = start, end, step
        self.bands = list(bands)
        self.update()

    def leaveEvent(self, event):
        self._hover_x = None
        self.update()

    def mouseMoveEvent(self, event):
        self._hover_x = event.pos().x()
        self.update()

    def _y_max(self):
        if self.fixed_max is not None:
            return self.fixed_max
        peak = max((v for d in self.data for _, v in d if v is not None), default=0)
        return nice_ceiling(max(peak * 1.1, self.min_y_max))

    def _ticks(self, span):
        interval, fmt = next(((i, f) for i, f in _TICKS if span / i <= 7), _TICKS[-1])
        first = _dt.datetime.fromtimestamp(self.start)
        if interval >= 86400:
            t = first.replace(hour=0, minute=0, second=0, microsecond=0) + _dt.timedelta(days=1)
            days = interval // 86400
            ticks = []
            while t.timestamp() <= self.end:
                ticks.append(t.timestamp())
                t += _dt.timedelta(days=days)
        else:
            # align to local clock boundaries (e.g. whole hours in UTC+5:30 too)
            offset = _time.localtime(self.start).tm_gmtoff
            t0 = (int(self.start + offset) // interval + 1) * interval - offset
            ticks = list(range(t0, int(self.end) + 1, interval))
        return ticks, fmt

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        font = self._font(8)
        fm = QFontMetrics(font)
        p.setFont(font)
        y_max = self._y_max()
        right_pad = fm.horizontalAdvance(self.formatter(y_max)) + 12
        plot = QRectF(0, fm.height() / 2 + 2, self.width() - right_pad, self.height() - fm.height() * 2 - 8)
        span = max(1, self.end - self.start)
        if plot.width() <= 10 or plot.height() <= 10:
            return

        def x_of(ts):
            return plot.left() + (ts - self.start) / span * plot.width()

        def y_of(v):
            return plot.bottom() - min(max(v, 0) / y_max, 1.0) * plot.height()

        # outage / highlight bands
        for s, e in self.bands:
            if e < self.start or s > self.end:
                continue
            x0, x1 = x_of(max(s, self.start)), x_of(min(e, self.end))
            p.fillRect(QRectF(x0, plot.top(), max(2.0, x1 - x0), plot.height()), theme.color("bad", 45))

        grid_pen = QPen(theme.color("grid"), 1, Qt.DashLine)
        for i in range(5):
            y = plot.top() + plot.height() * i / 4
            p.setPen(grid_pen)
            p.drawLine(QPointF(plot.left(), y), QPointF(plot.right(), y))
            p.setPen(theme.color("faint"))
            p.drawText(QRectF(plot.right() + 8, y - fm.height() / 2, right_pad, fm.height()),
                       Qt.AlignLeft | Qt.AlignVCenter, self.formatter(y_max * (4 - i) / 4))
        ticks, tick_fmt = self._ticks(span)
        for ts in ticks:
            x = x_of(ts)
            if x < plot.left() + 20 or x > plot.right() - 20:
                continue
            p.setPen(theme.color("faint"))
            p.drawText(QRectF(x - 40, plot.bottom() + 6, 80, fm.height()), Qt.AlignHCenter | Qt.AlignTop,
                       _dt.datetime.fromtimestamp(ts).strftime(tick_fmt))

        has_data = any(v is not None for d in self.data for _, v in d)
        if not has_data:
            p.setPen(theme.color("muted"))
            p.drawText(plot, Qt.AlignCenter, self.empty_text)
            return

        gap = self.step * 1.5 if not self.markers else float("inf")
        p.setClipRect(plot.adjusted(-4, -4, 4, 2))
        for (label_, color_key), points in zip(self.series, self.data):
            color = theme.color(color_key)
            segments, current, prev_ts = [], [], None
            for ts, v in points:
                if v is None or (prev_ts is not None and ts - prev_ts > gap):
                    if current:
                        segments.append(current)
                    current = []
                if v is not None:
                    current.append(QPointF(x_of(ts), y_of(v)))
                prev_ts = ts if v is not None else prev_ts
            if current:
                segments.append(current)
            for seg in segments:
                path = QPainterPath(seg[0])
                for pt in seg[1:]:
                    path.lineTo(pt)
                if len(seg) > 1 and not self.markers:
                    area = QPainterPath(path)
                    area.lineTo(QPointF(seg[-1].x(), plot.bottom()))
                    area.lineTo(QPointF(seg[0].x(), plot.bottom()))
                    area.closeSubpath()
                    grad = QLinearGradient(0, plot.top(), 0, plot.bottom())
                    grad.setColorAt(0, theme.color(color_key, 70))
                    grad.setColorAt(1, theme.color(color_key, 0))
                    p.fillPath(area, grad)
                p.setPen(QPen(color, 1.8))
                p.setBrush(Qt.NoBrush)
                if len(seg) > 1:
                    p.drawPath(path)
                if self.markers or len(seg) == 1:
                    p.setPen(QPen(theme.color("surface"), 1.5))
                    p.setBrush(color)
                    for pt in seg:
                        p.drawEllipse(pt, 3.5, 3.5)
        p.setClipping(False)

        if self._hover_x is not None and plot.left() <= self._hover_x <= plot.right():
            self._draw_hover(p, plot, x_of, y_of, font, fm)

    def _draw_hover(self, p, plot, x_of, y_of, font, fm):
        candidates = [ts for d in self.data for ts, v in d if v is not None]
        if not candidates:
            return
        target = self.start + (self._hover_x - plot.left()) / plot.width() * (self.end - self.start)
        ts = min(candidates, key=lambda t: abs(t - target))
        if abs(x_of(ts) - self._hover_x) > max(30.0, plot.width() / 40):
            return
        x = x_of(ts)
        lines = []
        for (label_, color_key), points in zip(self.series, self.data):
            value = next((v for t, v in points if t == ts), None)
            if value is not None:
                lines.append((color_key, f"{label_}  {self.formatter(value)}"))
                p.setPen(QPen(theme.color("surface"), 2))
                p.setBrush(theme.color(color_key))
                p.drawEllipse(QPointF(x, y_of(value)), 4, 4)
        if not lines:
            return
        p.setPen(QPen(theme.color("faint"), 1, Qt.DotLine))
        p.drawLine(QPointF(x, plot.top()), QPointF(x, plot.bottom()))
        when = _dt.datetime.fromtimestamp(ts)
        stamp = when.strftime("%d %b, %H:%M") if self.end - self.start > 86400 or self.markers else when.strftime("%H:%M")
        lines.insert(0, ("muted", stamp))
        width = max(fm.horizontalAdvance(t) for _, t in lines) + 34
        height = len(lines) * (fm.height() + 2) + 12
        bx = x + 12 if x + 12 + width < plot.right() else x - 12 - width
        box = QRectF(bx, plot.top() + 4, width, height)
        p.setPen(QPen(theme.color("border"), 1))
        p.setBrush(theme.color("surface2"))
        p.drawRoundedRect(box, 8, 8)
        p.setFont(font)
        for i, (color_key, text) in enumerate(lines):
            ty = box.top() + 6 + i * (fm.height() + 2)
            if i:
                p.setPen(Qt.NoPen)
                p.setBrush(theme.color(color_key))
                p.drawEllipse(QPointF(box.left() + 13, ty + fm.height() / 2), 3.5, 3.5)
            p.setPen(theme.color("text" if i else "muted"))
            p.drawText(QRectF(box.left() + (23 if i else 10), ty, width, fm.height()),
                       Qt.AlignLeft | Qt.AlignVCenter, text)
