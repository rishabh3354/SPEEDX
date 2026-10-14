"""Reusable layout building blocks."""

from PyQt5.QtCore import QPropertyAnimation, QRectF, QSize, Qt, pyqtProperty
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QAbstractButton, QFrame, QGridLayout, QHBoxLayout, QLabel, QScrollArea,
                             QSizePolicy, QVBoxLayout, QWidget)

from .. import icons
from ..theme import theme
from .charts import Sparkline


def label(text="", name=None, wrap=False, parent=None):
    lbl = QLabel(text, parent)
    if name:
        lbl.setObjectName(name)
    lbl.setWordWrap(wrap)
    return lbl


def divider():
    line = QFrame()
    line.setObjectName("Divider")
    return line


class IconLabel(QLabel):
    """A QLabel showing a themed line icon."""

    def __init__(self, name, color_key="muted", size=18, parent=None):
        super().__init__(parent)
        self._name, self._color, self._size = name, color_key, size
        self.setFixedSize(size, size)
        theme.changed.connect(self._refresh)
        self._refresh()

    def set_color(self, color_key):
        self._color = color_key
        self._refresh()

    def _refresh(self):
        self.setPixmap(icons.pixmap(self._name, theme.colors.get(self._color, self._color), self._size))


class Dot(QWidget):
    def __init__(self, color_key, size=8, parent=None):
        super().__init__(parent)
        self.color_key = color_key
        self.setFixedSize(size, size)
        theme.changed.connect(self.update)

    def set_color(self, color_key):
        self.color_key = color_key
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setBrush(theme.color(self.color_key))
        p.drawEllipse(QRectF(self.rect()))


class Card(QFrame):
    """Rounded surface with an optional header (title, hint, trailing widget)."""

    def __init__(self, title=None, hint=None, trailing=None, padding=18, spacing=12, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(padding, padding - 2, padding, padding)
        self.body.setSpacing(spacing)
        self.title_label = None
        self.hint_label = None
        if title or trailing is not None:
            header = QHBoxLayout()
            header.setSpacing(8)
            texts = QVBoxLayout()
            texts.setSpacing(1)
            if title:
                self.title_label = label(title, "CardTitle")
                texts.addWidget(self.title_label)
            if hint:
                self.hint_label = label(hint, "CardHint")
                texts.addWidget(self.hint_label)
            header.addLayout(texts, 1)
            if trailing is not None:
                header.addWidget(trailing, 0, Qt.AlignRight | Qt.AlignVCenter)
            self.body.addLayout(header)

    def add(self, widget, stretch=0):
        self.body.addWidget(widget, stretch)
        return widget

    def add_layout(self, layout, stretch=0):
        self.body.addLayout(layout, stretch)
        return layout


class StatCard(Card):
    """Headline metric: icon + title, large value with unit, caption and sparkline."""

    def __init__(self, title, icon_name, color_key, y_max=None, min_y_max=1.0, capacity=60, parent=None):
        super().__init__(padding=16, spacing=6, parent=parent)
        head = QHBoxLayout()
        head.setSpacing(8)
        self.icon = IconLabel(icon_name, color_key, 18)
        head.addWidget(self.icon)
        head.addWidget(label(title, "Label"), 1)
        self.badge = label("", "Chip")
        self.badge.hide()
        head.addWidget(self.badge)
        self.body.addLayout(head)

        row = QHBoxLayout()
        row.setSpacing(6)
        self.value = label("—", "BigValue")
        self.unit = label("", "Unit")
        row.addWidget(self.value)
        row.addWidget(self.unit, 0, Qt.AlignBottom)
        row.addStretch(1)
        self.body.addLayout(row)
        self.caption = label("", "Faint")
        self.body.addWidget(self.caption)
        self.spark = Sparkline(color_key, capacity=capacity, y_max=y_max, min_y_max=min_y_max)
        self.spark.setFixedHeight(54)
        self.body.addWidget(self.spark)

    def set(self, value, unit="", caption=None, badge=None):
        self.value.setText(value)
        self.unit.setText(unit)
        if caption is not None:
            self.caption.setText(caption)
        if badge is not None:
            self.badge.setText(badge)
            self.badge.setVisible(bool(badge))


class InfoGrid(QWidget):
    """Two column list of label / value pairs."""

    def __init__(self, rows=(), columns=1, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(18)
        self.grid.setVerticalSpacing(10)
        self.columns = columns
        self.values = {}
        for key, text in rows:
            self.add_row(key, text)

    def add_row(self, key, text, value="—"):
        idx = len(self.values)
        r, c = divmod(idx, self.columns)
        name = label(text, "Label")
        val = label(value, "Value")
        val.setTextInteractionFlags(Qt.TextSelectableByMouse)
        val.setWordWrap(True)
        self.grid.addWidget(name, r, c * 2)
        self.grid.addWidget(val, r, c * 2 + 1)
        self.grid.setColumnStretch(c * 2 + 1, 1)
        self.values[key] = val
        return val

    def set(self, key, value):
        if key in self.values:
            self.values[key].setText(value)


class Legend(QWidget):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)
        self.labels = []
        for text, color_key in items:
            box = QHBoxLayout()
            box.setSpacing(6)
            box.addWidget(Dot(color_key))
            lbl = label(text, "Label")
            self.labels.append(lbl)
            box.addWidget(lbl)
            lay.addLayout(box)


class Toggle(QAbstractButton):
    """iOS style switch."""

    def __init__(self, checked=False, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setChecked(checked)
        self.setCursor(Qt.PointingHandCursor)
        self._pos = 1.0 if checked else 0.0
        self._anim = QPropertyAnimation(self, b"knob", self)
        self._anim.setDuration(140)
        self.toggled.connect(self._animate)
        theme.changed.connect(self.update)

    def sizeHint(self):
        return QSize(40, 22)

    def _animate(self, checked):
        self._anim.stop()
        self._anim.setStartValue(self._pos)
        self._anim.setEndValue(1.0 if checked else 0.0)
        self._anim.start()

    def get_knob(self):
        return self._pos

    def set_knob(self, value):
        self._pos = value
        self.update()

    knob = pyqtProperty(float, get_knob, set_knob)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = QRectF(1, 1, 38, 20)
        p.setPen(Qt.NoPen)
        p.setBrush(theme.color("accent") if self.isChecked() else theme.color("border"))
        if not self.isEnabled():
            p.setOpacity(0.5)
        p.drawRoundedRect(r, 10, 10)
        p.setBrush(theme.color("accent_text") if self.isChecked() else theme.color("surface"))
        x = 3 + self._pos * 18
        p.drawEllipse(QRectF(x, 3, 16, 16))


class Page(QWidget):
    """Scrollable page with a title header."""

    def __init__(self, title, subtitle="", parent=None):
        super().__init__(parent)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        header = QHBoxLayout()
        header.setContentsMargins(28, 22, 28, 14)
        texts = QVBoxLayout()
        texts.setSpacing(2)
        texts.addWidget(label(title, "PageTitle"))
        self.subtitle = label(subtitle, "PageSubtitle")
        texts.addWidget(self.subtitle)
        header.addLayout(texts, 1)
        self.actions = QHBoxLayout()
        self.actions.setSpacing(8)
        header.addLayout(self.actions)
        outer.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        body = QWidget()
        body.setObjectName("PageBody")
        self.content = QVBoxLayout(body)
        self.content.setContentsMargins(28, 4, 28, 28)
        self.content.setSpacing(16)
        scroll.setWidget(body)
        outer.addWidget(scroll, 1)

    def add(self, widget, stretch=0):
        self.content.addWidget(widget, stretch)
        return widget

    def add_layout(self, layout, stretch=0):
        self.content.addLayout(layout, stretch)
        return layout

    def finish(self):
        self.content.addStretch(1)

    # pages override these
    def on_snapshot(self, snap, monitor):
        pass

    def on_shown(self):
        pass


def row(*widgets, spacing=16, stretches=None):
    lay = QHBoxLayout()
    lay.setSpacing(spacing)
    for i, w in enumerate(widgets):
        stretch = stretches[i] if stretches else 1
        if isinstance(w, QWidget):
            lay.addWidget(w, stretch)
        else:
            lay.addLayout(w, stretch)
    return lay


def expanding(widget):
    widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    return widget
