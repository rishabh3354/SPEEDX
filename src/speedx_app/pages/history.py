import time

from PyQt5.QtWidgets import QButtonGroup, QGridLayout, QHBoxLayout, QPushButton, QWidget

from .. import formatting as fmt
from ..history_store import RANGES
from ..widgets.charts import TimeSeriesChart
from ..widgets.common import Card, Legend, Page, label

REFRESH_TICKS = 30


def _avg(points):
    values = [v for _, v in points if v is not None]
    return sum(values) / len(values) if values else None


def _peak(points):
    return max((v for _, v in points if v is not None), default=None)


class _ChartCard(Card):
    def __init__(self, title, series, formatter, legend=False, **chart_kwargs):
        super().__init__(title, trailing=Legend(series) if legend else None)
        self.chart = TimeSeriesChart(series, formatter=formatter, **chart_kwargs)
        self.chart.setMinimumHeight(190)
        self.add(self.chart, 1)
        self.stats = label("", "Faint")
        self.add(self.stats)


class HistoryPage(Page):
    def __init__(self, ctx, has_battery):
        super().__init__("History", "What your system and connection did while you weren't watching")
        self.ctx = ctx
        self.range_key = "24h"
        self._tick = 0

        seg = QWidget()
        seg_lay = QHBoxLayout(seg)
        seg_lay.setContentsMargins(0, 0, 0, 0)
        seg_lay.setSpacing(0)
        self.range_group = QButtonGroup(self)
        for i, (key, text, _, _) in enumerate(RANGES):
            b = QPushButton(text)
            b.setObjectName("Segment")
            b.setCheckable(True)
            b.setChecked(key == self.range_key)
            b.setProperty("segment", "first" if i == 0 else "last" if i == len(RANGES) - 1 else "mid")
            self.range_group.addButton(b, i)
            seg_lay.addWidget(b)
        self.range_group.buttonClicked[int].connect(self._set_range)
        self.actions.addWidget(seg)

        speed = ctx.speed
        self.cards = {
            "cpu": _ChartCard("CPU usage", [("CPU", "cpu")], fmt.percent, y_max=100),
            "mem": _ChartCard("Memory", [("RAM", "mem"), ("Swap", "disk")], fmt.percent, legend=True, y_max=100),
            "net": _ChartCard("Network", [("Download", "down"), ("Upload", "up")], speed, legend=True,
                              min_y_max=10 * 1024),
            "latency": _ChartCard("Latency", [("Latency", "accent")], lambda v: f"{v:.0f} ms", min_y_max=50),
            "disk": _ChartCard("Disk activity", [("Read", "disk"), ("Write", "accent")],
                               lambda v: fmt.size(v) + "/s", legend=True, min_y_max=1024 * 1024),
            "temp": _ChartCard("CPU temperature", [("Temperature", "warn")], self._fmt_temp, min_y_max=60),
        }
        if has_battery:
            self.cards["battery"] = _ChartCard("Battery level", [("Battery", "good")], fmt.percent, y_max=100)
            self.cards["power"] = _ChartCard("Power draw", [("Power", "warn")], lambda v: f"{v:.1f} W",
                                             min_y_max=10)
        grid = QGridLayout()
        grid.setSpacing(16)
        for i, card in enumerate(self.cards.values()):
            grid.addWidget(card, i // 2, i % 2)
        self.add_layout(grid)
        self.note = label("SpeedX keeps one averaged sample per minute for 30 days. Gaps mean SpeedX was not "
                          "running or the computer was asleep. Red shading marks internet outages.",
                          "Faint", wrap=True)
        self.add(self.note)
        self.finish()

    def _fmt_temp(self, value):
        return fmt.temperature(value, self.ctx.config.get("temp_unit"))

    def _set_range(self, index):
        self.range_key = RANGES[index][0]
        self.refresh()

    def on_shown(self):
        self._tick = 0
        self.refresh()

    def on_snapshot(self, snap, monitor):
        self._tick += 1
        if self._tick % REFRESH_TICKS == 0:
            self.refresh()

    def refresh(self):
        key, _, seconds, bucket = next(r for r in RANGES if r[0] == self.range_key)
        end = time.time()
        start = end - seconds
        cols = ["cpu", "mem", "swap", "down", "up", "down_max", "up_max", "disk_read", "disk_write",
                "latency", "loss", "temp", "battery", "power"]
        d = self.ctx.history_store.query(cols, seconds, bucket)
        outages = [(o["start"], o["end"]) for o in self.ctx.outages.since(seconds)]
        last = self.ctx.monitor.last or {}
        if last.get("outage_since"):
            outages.append((last["outage_since"], end))

        def show(card_key, columns, bands=()):
            card = self.cards[card_key]
            card.chart.set_data([d[c] for c in columns], start, end, bucket, bands)
            return card

        card = show("cpu", ["cpu"])
        avg, peak = _avg(d["cpu"]), _peak(d["cpu"])
        card.stats.setText(f"Average {fmt.percent(avg)}  ·  Peak {fmt.percent(peak)}" if avg is not None else "")

        card = show("mem", ["mem", "swap"])
        avg, peak = _avg(d["mem"]), _peak(d["mem"])
        card.stats.setText(f"Average {fmt.percent(avg)}  ·  Peak {fmt.percent(peak)}" if avg is not None else "")

        card = show("net", ["down", "up"], outages)
        if _avg(d["down"]) is not None:
            unit = self.ctx.config.get("speed_unit")
            card.stats.setText(
                f"Average ↓ {fmt.speed(_avg(d['down']), unit)}  ↑ {fmt.speed(_avg(d['up']), unit)}  ·  "
                f"Peak ↓ {fmt.speed(_peak(d['down_max']) or 0, unit)}  ↑ {fmt.speed(_peak(d['up_max']) or 0, unit)}")
        else:
            card.stats.setText("")

        card = show("latency", ["latency"], outages)
        avg, loss = _avg(d["latency"]), _avg(d["loss"])
        offline = sum(min(e, end) - max(s, start) for s, e in outages)
        parts = []
        if avg is not None:
            parts.append(f"Average {avg:.0f} ms")
        if loss is not None:
            parts.append(f"Packet loss {loss:.1f}%")
        parts.append(f"{len(outages)} outage{'s' if len(outages) != 1 else ''}"
                     + (f" ({fmt.duration_precise(offline)} offline)" if outages else ""))
        card.stats.setText("  ·  ".join(parts))

        card = show("disk", ["disk_read", "disk_write"])
        if _avg(d["disk_read"]) is not None:
            card.stats.setText(f"Average read {fmt.size(_avg(d['disk_read']))}/s  ·  "
                               f"write {fmt.size(_avg(d['disk_write']))}/s")

        card = show("temp", ["temp"])
        avg, peak = _avg(d["temp"]), _peak(d["temp"])
        card.setVisible(avg is not None or bool(self.ctx.monitor.history["temp"]))
        if avg is not None:
            card.stats.setText(f"Average {self._fmt_temp(avg)}  ·  Peak {self._fmt_temp(peak)}")

        if "battery" in self.cards:
            card = show("battery", ["battery"])
            low = min((v for _, v in d["battery"] if v is not None), default=None)
            card.stats.setText(f"Lowest {fmt.percent(low)}" if low is not None else "")
            card = show("power", ["power"])
            avg = _avg(d["power"])
            card.stats.setText(f"Average {avg:.1f} W" if avg is not None else "")
