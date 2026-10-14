from .. import formatting as fmt
from ..widgets.charts import LineChart, MeterBar, RingGauge
from ..widgets.common import Card, InfoGrid, Legend, Page, row
from .overview import _ProcessList, level_color


class MemoryPage(Page):
    needs_processes = True

    def __init__(self, ctx):
        super().__init__("Memory", "RAM and swap usage")
        self.ctx = ctx

        self.ram_ring = RingGauge("mem", thickness=14)
        self.ram_ring.setMinimumSize(180, 180)
        ram_card = Card("RAM")
        ram_card.add(self.ram_ring, 1)

        self.swap_ring = RingGauge("disk", thickness=14)
        self.swap_ring.setMinimumSize(180, 180)
        swap_card = Card("Swap")
        swap_card.add(self.swap_ring, 1)

        self.info = InfoGrid([
            ("total", "Total"), ("used", "In use"), ("available", "Available"),
            ("cached", "Cached / buffers"), ("swap_total", "Swap size"), ("swap_used", "Swap used"),
        ])
        self.bar = MeterBar("mem", 10)
        info_card = Card("Breakdown")
        info_card.add(self.bar)
        info_card.add(self.info)
        info_card.body.addStretch(1)
        self.add_layout(row(ram_card, swap_card, info_card, stretches=[1, 1, 1]))

        self.chart = LineChart([("RAM", "mem"), ("Swap", "disk")], y_max=100)
        self.chart.setMinimumHeight(230)
        chart_card = Card("Usage history", "Last 2 minutes",
                          trailing=Legend([("RAM", "mem"), ("Swap", "disk")]))
        chart_card.add(self.chart, 1)

        self.procs = _ProcessList(7)
        proc_card = Card("Top memory consumers")
        proc_card.add(self.procs)
        proc_card.body.addStretch(1)
        self.add_layout(row(chart_card, proc_card, stretches=[2, 1]))
        self.finish()

    def on_snapshot(self, snap, monitor):
        mem, swap = snap["mem"], snap["swap"]
        self.ram_ring.color_key = level_color(mem["percent"], "mem")
        self.ram_ring.set_value(mem["percent"], f"{mem['percent']:.0f}%", f"{fmt.size(mem['used'])} used")
        if swap["total"]:
            self.swap_ring.set_value(swap["percent"], f"{swap['percent']:.0f}%", f"{fmt.size(swap['used'])} used")
        else:
            self.swap_ring.set_value(0, "Off", "no swap")
        self.bar.set_fraction(mem["percent"] / 100, level_color(mem["percent"], "mem"))
        self.info.set("total", fmt.size(mem["total"]))
        self.info.set("used", fmt.size(mem["used"]))
        self.info.set("available", fmt.size(mem["available"]))
        self.info.set("cached", fmt.size(mem["cached"]))
        self.info.set("swap_total", fmt.size(swap["total"]) if swap["total"] else "Disabled")
        self.info.set("swap_used", fmt.size(swap["used"]))
        self.chart.set_data(monitor.history["mem"], monitor.history["swap"], capacity=monitor.history["mem"].maxlen)
        if monitor.processes:
            top = sorted(monitor.processes, key=lambda r: r[4], reverse=True)[:7]
            self.procs.set_rows([(r[1], fmt.percent(r[3]), fmt.size(r[4])) for r in top])
