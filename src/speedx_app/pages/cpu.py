from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget

from .. import formatting as fmt
from ..widgets.charts import LineChart, RingGauge, Sparkline
from ..widgets.common import Card, InfoGrid, Page, label, row
from .overview import level_color


class _CoreTile(QWidget):
    def __init__(self, index, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)
        head = QHBoxLayout()
        head.addWidget(label(f"Core {index}", "Label"), 1)
        self.value = label("0%", "Value")
        head.addWidget(self.value)
        lay.addLayout(head)
        self.spark = Sparkline("cpu", capacity=60, y_max=100)
        self.spark.setFixedHeight(38)
        lay.addWidget(self.spark)

    def update_core(self, value, history):
        self.value.setText(f"{value:.0f}%")
        self.spark.set_color(level_color(value, "cpu"))
        self.spark.set_data(history)


class CpuPage(Page):
    def __init__(self, ctx):
        super().__init__("CPU", ctx.monitor.info["cpu_model"])
        self.ctx = ctx
        info = ctx.monitor.info

        self.ring = RingGauge("cpu", thickness=14)
        self.ring.setMinimumSize(190, 190)
        ring_card = Card("Utilization")
        ring_card.add(self.ring, 1)

        self.info = InfoGrid([
            ("model", "Processor"), ("cores", "Cores / threads"), ("freq", "Frequency"),
            ("temp", "Temperature"), ("load", "Load average"), ("uptime", "Uptime"),
            ("arch", "Architecture"), ("kernel", "Kernel"),
        ], columns=2)
        self.info.set("model", info["cpu_model"])
        self.info.set("cores", f"{info['cores']} cores · {info['threads']} threads")
        self.info.set("arch", info["arch"])
        self.info.set("kernel", info["kernel"])
        info_card = Card("Details")
        info_card.add(self.info)
        info_card.body.addStretch(1)
        self.add_layout(row(ring_card, info_card, stretches=[1, 2]))

        self.chart = LineChart([("CPU", "cpu")], y_max=100)
        self.chart.setMinimumHeight(220)
        chart_card = Card("Usage history", "Last 2 minutes")
        chart_card.add(self.chart, 1)

        self.temp_chart = LineChart([("Temp", "warn")], min_y_max=60, formatter=self._fmt_temp)
        self.temp_chart.setMinimumHeight(220)
        self.temp_card = Card("Temperature", "Last 2 minutes")
        self.temp_card.add(self.temp_chart, 1)
        self.add_layout(row(chart_card, self.temp_card, stretches=[2, 1]))

        self.cores_card = Card("Per-core usage", f"{info['threads']} logical processors")
        self.cores_grid = QGridLayout()
        self.cores_grid.setHorizontalSpacing(22)
        self.cores_grid.setVerticalSpacing(14)
        self.cores_card.add_layout(self.cores_grid)
        self.tiles = []
        self.add(self.cores_card)
        self.finish()

    def _fmt_temp(self, value):
        return fmt.temperature(value, self.ctx.config.get("temp_unit"))

    def on_snapshot(self, snap, monitor):
        cpu = snap["cpu"]
        self.ring.color_key = level_color(cpu, "cpu")
        self.ring.set_value(cpu, f"{cpu:.0f}%", "in use")
        self.info.set("freq", fmt.frequency(snap["cpu_freq"]))
        temp = snap["cpu_temp"]
        self.info.set("temp", fmt.temperature(temp, self.ctx.config.get("temp_unit")) if temp is not None
                      else "Sensor not available")
        self.info.set("load", "  ".join(f"{v:.2f}" for v in snap["load"]))
        self.info.set("uptime", fmt.duration(snap["uptime"]))
        self.chart.set_data(monitor.history["cpu"], capacity=monitor.history["cpu"].maxlen)
        self.temp_card.setVisible(temp is not None)
        if temp is not None:
            self.temp_chart.set_data(monitor.history["temp"], capacity=monitor.history["temp"].maxlen)

        cores = snap["cpu_cores"]
        if len(self.tiles) != len(cores):
            for tile in self.tiles:
                tile.setParent(None)
            cols = 4 if len(cores) > 8 else max(2, min(4, len(cores)))
            self.tiles = [_CoreTile(i) for i in range(len(cores))]
            for i, tile in enumerate(self.tiles):
                self.cores_grid.addWidget(tile, i // cols, i % cols)
        for tile, value, hist in zip(self.tiles, cores, monitor.core_history):
            tile.update_core(value, hist)
