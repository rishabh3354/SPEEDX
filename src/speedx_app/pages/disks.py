from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget

from .. import formatting as fmt
from ..widgets.charts import LineChart, MeterBar
from ..widgets.common import Card, Legend, Page, StatCard, label
from .overview import level_color


class _PartitionRow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(7)
        top = QHBoxLayout()
        self.mount = label("", "Value")
        self.meta = label("", "Faint")
        self.usage = label("", "Muted")
        top.addWidget(self.mount)
        top.addWidget(self.meta, 1)
        top.addWidget(self.usage)
        lay.addLayout(top)
        self.bar = MeterBar("disk", 10)
        lay.addWidget(self.bar)

    def set(self, part):
        self.mount.setText(part["mount"])
        self.meta.setText(f"   {part['device']} · {part['fstype']}")
        self.usage.setText(f"{fmt.size(part['free'])} free of {fmt.size(part['total'])}  ·  {part['percent']:.0f}%")
        self.bar.set_fraction(part["percent"] / 100, level_color(part["percent"], "disk"))


class DisksPage(Page):
    def __init__(self, ctx):
        super().__init__("Disks", "Storage space and disk activity")
        self.ctx = ctx

        self.read_card = StatCard("Read", "down", "disk", min_y_max=1024 * 1024)
        self.write_card = StatCard("Write", "up", "accent", min_y_max=1024 * 1024)
        self.space_card = StatCard("Total storage", "disk", "good", y_max=100)
        tiles = QGridLayout()
        tiles.setSpacing(16)
        for i, card in enumerate((self.read_card, self.write_card, self.space_card)):
            tiles.addWidget(card, 0, i)
        self.add_layout(tiles)
        self.space_card.spark.hide()
        self.space_card.body.addStretch(1)

        self.chart = LineChart([("Read", "disk"), ("Write", "accent")], min_y_max=1024 * 1024,
                               formatter=lambda v: fmt.size(v) + "/s")
        self.chart.setMinimumHeight(230)
        chart_card = Card("Disk activity", "Last 2 minutes", trailing=Legend([("Read", "disk"), ("Write", "accent")]))
        chart_card.add(self.chart, 1)
        self.add(chart_card)

        self.parts_card = Card("Volumes", "Mounted file systems")
        self.parts_box = QVBoxLayout()
        self.parts_box.setSpacing(18)
        self.parts_card.add_layout(self.parts_box)
        self.add(self.parts_card)
        self.rows = []
        self.finish()

    def on_snapshot(self, snap, monitor):
        h = monitor.history
        self.read_card.set(fmt.size(snap["disk_read"]).split()[0], fmt.size(snap["disk_read"]).split()[1] + "/s")
        self.read_card.spark.set_data(h["disk_read"])
        self.write_card.set(fmt.size(snap["disk_write"]).split()[0], fmt.size(snap["disk_write"]).split()[1] + "/s")
        self.write_card.spark.set_data(h["disk_write"])
        self.chart.set_data(h["disk_read"], h["disk_write"], capacity=h["disk_read"].maxlen)

        parts = monitor.partitions
        total = sum(p["total"] for p in parts)
        used = sum(p["used"] for p in parts)
        free = sum(p["free"] for p in parts)
        if total:
            self.space_card.set(fmt.size(free).split()[0], fmt.size(free).split()[1] + " free",
                                f"{fmt.size(used)} used of {fmt.size(total)} on {len(parts)} volume(s)")
        while len(self.rows) < len(parts):
            r = _PartitionRow()
            self.rows.append(r)
            self.parts_box.addWidget(r)
        for i, r in enumerate(self.rows):
            if i < len(parts):
                r.set(parts[i])
                r.show()
            else:
                r.hide()
