import datetime as dt

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget

from .. import formatting as fmt
from ..battery import status_text
from ..netinfo import signal_quality
from ..widgets.charts import LineChart, MeterBar
from ..widgets.common import Card, InfoGrid, Legend, Page, StatCard, label, row


def level_color(percent, base):
    if percent >= 90:
        return "bad"
    if percent >= 75:
        return "warn"
    return base


class _ProcessList(QWidget):
    def __init__(self, count=6, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(12)
        self.grid.setVerticalSpacing(9)
        for c, text in enumerate(("Process", "CPU", "Memory")):
            h = label(text, "Faint")
            self.grid.addWidget(h, 0, c, Qt.AlignRight if c else Qt.AlignLeft)
        self.rows = []
        for r in range(count):
            cells = [label("", "Value" if c == 0 else "Muted") for c in range(3)]
            for c, cell in enumerate(cells):
                self.grid.addWidget(cell, r + 1, c, Qt.AlignRight if c else Qt.AlignLeft)
            self.rows.append(cells)
        self.grid.setColumnStretch(0, 1)

    def set_rows(self, rows):
        for i, cells in enumerate(self.rows):
            if i < len(rows):
                name, cpu, mem = rows[i]
                cells[0].setText(name)
                cells[1].setText(cpu)
                cells[2].setText(mem)
            else:
                for cell in cells:
                    cell.setText("")


class OverviewPage(Page):
    needs_processes = True

    def __init__(self, ctx):
        super().__init__("Overview", "Live snapshot of your system and connection")
        self.ctx = ctx

        self.cpu_card = StatCard("CPU", "cpu", "cpu", y_max=100)
        self.mem_card = StatCard("Memory", "memory", "mem", y_max=100)
        self.down_card = StatCard("Download", "down", "down", min_y_max=10 * 1024)
        self.up_card = StatCard("Upload", "up", "up", min_y_max=10 * 1024)
        tiles = QGridLayout()
        tiles.setSpacing(16)
        for i, card in enumerate((self.cpu_card, self.mem_card, self.down_card, self.up_card)):
            tiles.addWidget(card, 0, i)
        self.add_layout(tiles)

        # network chart + system info
        self.net_chart = LineChart([("Download", "down"), ("Upload", "up")], min_y_max=10 * 1024,
                                   formatter=ctx.speed)
        self.net_chart.setMinimumHeight(220)
        net_card = Card("Network activity", "Last 2 minutes",
                        trailing=Legend([("Download", "down"), ("Upload", "up")]))
        net_card.add(self.net_chart, 1)

        self.info = InfoGrid([
            ("host", "Device"), ("os", "System"), ("uptime", "Uptime"), ("ip", "Local IP"),
            ("conn", "Connection"), ("link", "Network"), ("today", "Data today"),
        ])
        if ctx.has_battery:
            self.info.add_row("battery", "Battery")
        info_card = Card("System")
        info_card.add(self.info)
        info_card.body.addStretch(1)
        self.info.set("host", ctx.monitor.info["hostname"])
        self.info.set("os", ctx.monitor.info["os"])
        self.add_layout(row(net_card, info_card, stretches=[2, 1]))

        # processes + storage
        self.procs = _ProcessList()
        proc_card = Card("Top processes", "Sorted by CPU usage")
        proc_card.add(self.procs)
        proc_card.body.addStretch(1)

        self.storage_card = Card("Storage")
        self.storage_box = QVBoxLayout()
        self.storage_box.setSpacing(14)
        self.storage_card.add_layout(self.storage_box)
        self.storage_card.body.addStretch(1)
        self._storage_rows = {}
        self.add_layout(row(proc_card, self.storage_card))
        self.finish()

    def _update_storage(self, partitions):
        for mount, widgets in list(self._storage_rows.items()):
            if mount not in {p["mount"] for p in partitions}:
                widgets[0].setParent(None)
                del self._storage_rows[mount]
        for part in partitions[:5]:
            if part["mount"] not in self._storage_rows:
                w = QWidget()
                lay = QVBoxLayout(w)
                lay.setContentsMargins(0, 0, 0, 0)
                lay.setSpacing(6)
                top = QHBoxLayout()
                name = label(part["mount"], "Value")
                detail = label("", "Muted")
                top.addWidget(name, 1)
                top.addWidget(detail)
                bar = MeterBar("disk")
                lay.addLayout(top)
                lay.addWidget(bar)
                self.storage_box.addWidget(w)
                self._storage_rows[part["mount"]] = (w, detail, bar)
            _, detail, bar = self._storage_rows[part["mount"]]
            detail.setText(f"{fmt.size(part['used'])} of {fmt.size(part['total'])}")
            bar.set_fraction(part["percent"] / 100, level_color(part["percent"], "disk"))

    def on_snapshot(self, snap, monitor):
        h = monitor.history
        cfg = self.ctx.config
        cpu = snap["cpu"]
        caption = []
        if snap["cpu_temp"] is not None:
            caption.append(fmt.temperature(snap["cpu_temp"], cfg.get("temp_unit")))
        if snap["cpu_freq"]:
            caption.append(fmt.frequency(snap["cpu_freq"]))
        caption.append(f"{monitor.info['threads']} threads")
        self.cpu_card.set(f"{cpu:.0f}", "%", "  ·  ".join(caption))
        self.cpu_card.spark.set_data(h["cpu"])

        mem = snap["mem"]
        self.mem_card.set(f"{mem['percent']:.0f}", "%", f"{fmt.size(mem['used'])} of {fmt.size(mem['total'])}")
        self.mem_card.spark.set_data(h["mem"])

        unit = cfg.get("speed_unit")
        num, u = fmt.speed_parts(snap["net_down"], unit)
        self.down_card.set(num, u, f"Peak {fmt.speed(monitor.peak_down, unit)}")
        self.down_card.spark.set_data(h["down"])
        num, u = fmt.speed_parts(snap["net_up"], unit)
        self.up_card.set(num, u, f"Peak {fmt.speed(monitor.peak_up, unit)}")
        self.up_card.spark.set_data(h["up"])

        self.net_chart.set_data(h["down"], h["up"], capacity=h["down"].maxlen)

        self.info.set("uptime", fmt.duration(snap["uptime"]))
        self.info.set("ip", self.ctx.local_ip or "—")
        if snap["online"] is None:
            conn = "Checking…"
        elif snap["online"]:
            conn = f"Online  ·  {snap['latency']:.0f} ms"
            if snap.get("loss"):
                conn += f"  ·  {snap['loss'] * 100:.0f}% loss"
        else:
            conn = "Offline"
        self.info.set("conn", conn)
        net = monitor.netinfo
        if net.get("type") == "wifi":
            name = net.get("ssid") or net.get("name") or "Wi-Fi"
            quality, _ = signal_quality(net.get("signal_dbm"), net.get("signal_pct"))
            link = f"Wi-Fi “{name}”" + (f"  ·  {quality} signal" if quality else "")
        elif net.get("type") == "ethernet":
            link = "Ethernet" + (f"  ·  {net['bitrate']:.0f} Mbps" if net.get("bitrate") else "")
        else:
            link = net.get("name") or ("Not connected" if net else "—")
        self.info.set("link", link)
        battery = snap.get("battery")
        if battery and battery.get("percent") is not None:
            text = f"{battery['percent']:.0f}%  ·  {status_text(battery).split(' (')[0]}"
            if battery.get("time_left") and battery.get("status") == "Discharging":
                text += f"  ·  {fmt.duration_precise(battery['time_left'])} left"
            self.info.set("battery", text)
        rx, tx = self.ctx.usage.day(dt.date.today())
        self.info.set("today", f"↓ {fmt.data(rx)}   ↑ {fmt.data(tx)}")

        if monitor.processes:
            top = sorted(monitor.processes, key=lambda r: r[3], reverse=True)[:6]
            self.procs.set_rows([(r[1], fmt.percent(r[3]), fmt.size(r[4])) for r in top])
        if snap["partitions"] is not None or not self._storage_rows:
            self._update_storage(monitor.partitions)
