import datetime as dt
import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAbstractItemView, QComboBox, QGridLayout, QHBoxLayout, QHeaderView, QPushButton,
                             QTableWidget, QTableWidgetItem, QWidget)

from .. import formatting as fmt
from .. import system
from ..export import save_csv
from ..connectivity import HOSTS, PROBE_INTERVAL
from ..netinfo import signal_quality
from ..theme import theme
from ..widgets.charts import LineChart, MeterBar
from ..widgets.common import Card, InfoGrid, Legend, Page, StatCard, label, row

OUTAGE_ROWS = 50


def loss_color(loss):
    if loss is None:
        return "muted"
    return "good" if loss < 0.01 else "warn" if loss < 0.05 else "bad"


def quality_verdict(latency, jitter, loss):
    """Plain language rating of the connection for real-time use (calls, games)."""
    if latency is None:
        return "Waiting for measurements…", "muted"
    loss = loss or 0.0
    jitter = jitter or 0.0
    if loss >= 0.05 or latency >= 200:
        return "Poor — expect choppy video calls, lag in games and slow page loads.", "bad"
    if loss >= 0.01 or latency >= 100 or jitter >= 30:
        return "Fair — fine for browsing and streaming; calls and games may stutter.", "warn"
    if latency < 40 and jitter < 10:
        return "Excellent — great for gaming, video calls and streaming.", "good"
    return "Good — smooth browsing, streaming and video calls.", "good"


class NetworkPage(Page):
    def __init__(self, ctx):
        super().__init__("Network", "Bandwidth, connection quality, Wi-Fi and outages")
        self.ctx = ctx

        self.iface = QComboBox()
        self.iface.setMinimumWidth(180)
        self.iface.setToolTip("Network interface to monitor")
        self.actions.addWidget(label("Interface", "Muted"))
        self.actions.addWidget(self.iface)
        self._fill_interfaces()
        self.iface.currentIndexChanged.connect(self._iface_changed)

        self.down_card = StatCard("Download", "down", "down", min_y_max=10 * 1024)
        self.up_card = StatCard("Upload", "up", "up", min_y_max=10 * 1024)
        self.ping_card = StatCard("Latency", "ping", "accent", min_y_max=50)
        tiles = QGridLayout()
        tiles.setSpacing(16)
        for i, card in enumerate((self.down_card, self.up_card, self.ping_card)):
            tiles.addWidget(card, 0, i)
        self.add_layout(tiles)

        self.chart = LineChart([("Download", "down"), ("Upload", "up")], min_y_max=10 * 1024, formatter=ctx.speed)
        self.chart.setMinimumHeight(240)
        chart_card = Card("Bandwidth", "Last 2 minutes", trailing=Legend([("Download", "down"), ("Upload", "up")]))
        chart_card.add(self.chart, 1)
        self.add(chart_card)

        self.add_layout(row(self._build_link_card(), self._build_quality_card()))
        self.add(self._build_outage_card())

        self.session = InfoGrid([
            ("rx", "Downloaded"), ("tx", "Uploaded"), ("peak_down", "Peak download"), ("peak_up", "Peak upload"),
        ])
        session_card = Card("This session", "Since SpeedX was started")
        session_card.add(self.session)
        session_card.body.addStretch(1)

        self.conn = InfoGrid([("ip", "Local IP"), ("iface", "Interface"), ("mac", "MAC address")])
        conn_card = Card("Adapter")
        conn_card.add(self.conn)
        conn_card.body.addStretch(1)
        self.add_layout(row(session_card, conn_card))
        self.finish()
        self._details_tick = 0
        self._outage_count = None

    # ------------------------------------------------------------ building
    def _build_link_card(self):
        self.link_card = Card("Wi-Fi")
        self.link_info = InfoGrid([
            ("network", "Network"), ("signal", "Signal"), ("band", "Band"), ("rate", "Link rate"),
        ])
        self.signal_bar = MeterBar("good", 8)
        self.link_card.add(self.signal_bar)
        self.link_card.add(self.link_info)
        self.link_tip = label("", "Faint", wrap=True)
        self.link_card.add(self.link_tip)
        self.link_card.body.addStretch(1)
        return self.link_card

    def _build_quality_card(self):
        self.quality = InfoGrid([("latency", "Average latency"), ("jitter", "Jitter"), ("loss", "Packet loss")])
        self.quality_chart = LineChart([("Latency", "accent")], capacity=60, min_y_max=50,
                                       formatter=lambda v: f"{v:.0f} ms")
        self.quality_chart.setMinimumHeight(120)
        self.verdict = label("", "Muted", wrap=True)
        card = Card("Connection quality", "Loss and jitter over the last minute")
        card.add(self.quality)
        card.add(self.verdict)
        card.add(self.quality_chart, 1)
        self.method_label = label("", "Faint", wrap=True)
        card.add(self.method_label)
        return card

    def _build_outage_card(self):
        clear = QPushButton("Clear log")
        clear.setObjectName("Link")
        clear.clicked.connect(self._clear_outages)
        self.outage_export = QPushButton("Export CSV")
        self.outage_export.setObjectName("Link")
        self.outage_export.clicked.connect(self._export_outages)
        buttons = QWidget()
        b_lay = QHBoxLayout(buttons)
        b_lay.setContentsMargins(0, 0, 0, 0)
        b_lay.setSpacing(4)
        b_lay.addWidget(self.outage_export)
        b_lay.addWidget(clear)
        card = Card("Outages", "Times your internet went down", trailing=buttons)
        self.outage_summary = label("", "Value", wrap=True)
        card.add(self.outage_summary)
        self.outage_table = QTableWidget(0, 4)
        self.outage_table.setHorizontalHeaderLabels(["Started", "Ended", "Duration", "Cause"])
        self.outage_table.verticalHeader().hide()
        self.outage_table.setShowGrid(False)
        self.outage_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.outage_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.outage_table.setFocusPolicy(Qt.NoFocus)
        self.outage_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.outage_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.outage_table.verticalHeader().setDefaultSectionSize(34)
        card.add(self.outage_table)
        return card

    # ----------------------------------------------------------- interfaces
    def _fill_interfaces(self):
        current = self.ctx.config.get("interface")
        self.iface.blockSignals(True)
        self.iface.clear()
        self.iface.addItem("All adapters", "")
        for name in system.network_interfaces():
            self.iface.addItem(name, name)
        idx = self.iface.findData(current)
        self.iface.setCurrentIndex(max(idx, 0))
        self.iface.blockSignals(False)

    def _iface_changed(self):
        self.ctx.config.set("interface", self.iface.currentData() or "")

    def on_shown(self):
        self._fill_interfaces()
        self._details_tick = 0
        self._outage_count = None

    def _update_adapter(self, info):
        self.ctx.local_ip = system.local_ip()
        self.conn.set("ip", self.ctx.local_ip or "—")
        name = self.ctx.config.get("interface") or info.get("iface")
        details = {d["name"]: d for d in system.interface_details()}
        d = details.get(name)
        if d:
            self.conn.set("iface", d["name"] + ("" if d["up"] else " (down)"))
            self.conn.set("mac", d["mac"] or "—")
        else:
            self.conn.set("iface", "—")
            self.conn.set("mac", "—")

    # ---------------------------------------------------------------- link
    def _update_link(self, info):
        kind = info.get("type")
        rate = info.get("bitrate")
        rate_text = f"{rate:.0f} Mbps" if rate else "—"
        tip = ""
        if kind == "wifi":
            self.link_card.title_label.setText("Wi-Fi")
            dbm, pct = info.get("signal_dbm"), info.get("signal_pct")
            quality, color = signal_quality(dbm, pct)
            parts = [p for p in (f"{dbm:.0f} dBm" if dbm is not None else None,
                                 f"{pct}%" if pct is not None else None, quality) if p]
            self.link_info.set("network", info.get("ssid") or info.get("name") or info.get("iface") or "—")
            self.link_info.set("signal", "  ·  ".join(parts) or "—")
            if pct is None and dbm is not None:
                pct = max(0, min(100, 2 * (dbm + 100)))
            self.signal_bar.set_fraction((pct or 0) / 100, color)
            self.signal_bar.show()
            band, channel = info.get("band"), info.get("channel")
            self.link_info.set("band", f"{band} · channel {channel}" if band and channel else band or "—")
            self.link_info.set("rate", rate_text)
            if quality == "Weak":
                tip = ("Weak signal can make your connection slow and unstable. Move closer to the router "
                       "or remove obstacles between you and it.")
            elif quality == "Fair":
                tip = "Signal is fair. Moving closer to the router can improve speed and stability."
            elif band == "2.4 GHz":
                tip = "You're on 2.4 GHz. If your router offers 5 GHz, it is usually much faster nearby."
            elif rate:
                tip = "Link rate is the speed between this device and the router, not your internet speed."
        elif kind == "ethernet":
            self.link_card.title_label.setText("Ethernet")
            self.signal_bar.hide()
            self.link_info.set("network", info.get("name") or info.get("iface") or "Wired")
            self.link_info.set("signal", "Wired connection")
            self.link_info.set("band", "—")
            self.link_info.set("rate", rate_text)
            if rate and rate < 1000:
                tip = f"Link runs at {rate:.0f} Mbps. A Cat5e or better cable and gigabit port allow 1000 Mbps."
        else:
            self.link_card.title_label.setText("Network link")
            self.signal_bar.hide()
            self.link_info.set("network", info.get("name") or ("Not connected" if kind is None else "—"))
            for key in ("signal", "band", "rate"):
                self.link_info.set(key, "—")
        self.link_tip.setText(tip)
        self.link_tip.setVisible(bool(tip))

    # ------------------------------------------------------------- outages
    def _export_outages(self):
        rows = []
        for o in self.ctx.outages.items:
            rows.append([dt.datetime.fromtimestamp(o["start"]).isoformat(timespec="seconds"),
                         dt.datetime.fromtimestamp(o["end"]).isoformat(timespec="seconds"),
                         round(o["end"] - o["start"]), o.get("reason", ""), o.get("note", "")])
        save_csv(self, "speedx-outages", ["start", "end", "duration_seconds", "cause", "note"], rows,
                 self.outage_export)

    def _clear_outages(self):
        self.ctx.outages.clear()
        self._outage_count = None

    def _update_outages(self, snap):
        log = self.ctx.outages
        ongoing = snap.get("outage_since")
        key = (len(log.items), ongoing is not None)
        if key == self._outage_count and not ongoing:
            return
        self._outage_count = key

        week = log.since(7 * 86400)
        total = sum(o["end"] - o["start"] for o in week)
        if ongoing:
            self.outage_summary.setText(f"Offline right now — for {fmt.duration_precise(time.time() - ongoing)}"
                                        f" ({snap.get('outage_reason') or 'no connection'}).")
            self.outage_summary.setStyleSheet(f"color: {theme.colors['bad']};")
        elif week:
            self.outage_summary.setText(f"{len(week)} outage{'s' if len(week) != 1 else ''} in the last 7 days, "
                                        f"{fmt.duration_precise(total)} offline in total.")
            self.outage_summary.setStyleSheet(f"color: {theme.colors['warn']};")
        else:
            self.outage_summary.setText("No outages in the last 7 days.")
            self.outage_summary.setStyleSheet(f"color: {theme.colors['good']};")

        rows = []
        if ongoing:
            rows.append((ongoing, None, snap.get("outage_reason") or "", ""))
        rows += [(o["start"], o["end"], o.get("reason", ""), o.get("note", "")) for o in log.items[:OUTAGE_ROWS]]
        self.outage_table.setRowCount(len(rows))
        for r, (start, end, reason, note) in enumerate(rows):
            started = dt.datetime.fromtimestamp(start)
            if end is None:
                ended, length = "Ongoing", fmt.duration_precise(time.time() - start)
            else:
                ended_dt = dt.datetime.fromtimestamp(end)
                ended = ended_dt.strftime("%H:%M:%S" if ended_dt.date() == started.date() else "%d %b, %H:%M")
                length = fmt.duration_precise(end - start)
            cause = reason + (f" ({note})" if note else "")
            for c, text in enumerate((started.strftime("%d %b, %H:%M:%S"), ended, length, cause)):
                self.outage_table.setItem(r, c, QTableWidgetItem(text))
        header = self.outage_table.horizontalHeader().sizeHint().height()
        visible = min(len(rows), 8)
        self.outage_table.setFixedHeight(header + visible * self.outage_table.verticalHeader().defaultSectionSize() + 4)
        self.outage_table.setVisible(bool(rows))

    # ------------------------------------------------------------- refresh
    def on_snapshot(self, snap, monitor):
        unit = self.ctx.config.get("speed_unit")
        h = monitor.history
        num, u = fmt.speed_parts(snap["net_down"], unit)
        self.down_card.set(num, u, f"Peak {fmt.speed(monitor.peak_down, unit)}")
        self.down_card.spark.set_data(h["down"])
        num, u = fmt.speed_parts(snap["net_up"], unit)
        self.up_card.set(num, u, f"Peak {fmt.speed(monitor.peak_up, unit)}")
        self.up_card.spark.set_data(h["up"])
        self.chart.set_data(h["down"], h["up"], capacity=h["down"].maxlen)

        latency, jitter, loss = snap["latency"], snap.get("jitter"), snap.get("loss")
        if snap.get("outage_since"):
            self.ping_card.set("—", "", f"Offline for {fmt.duration_precise(time.time() - snap['outage_since'])}")
        elif latency is None:
            self.ping_card.set("—", "", "Checking connection…")
        else:
            caption = f"Jitter {jitter:.0f} ms" if jitter is not None else "Measuring jitter…"
            if loss is not None:
                caption += f"  ·  {loss * 100:.0f}% loss"
            self.ping_card.set(f"{latency:.0f}", "ms", caption)
        self.ping_card.spark.set_data(monitor.latency_history)

        history = list(monitor.latency_history)[-30:]
        avg = sum(history) / len(history) if history else None
        self.quality.set("latency", f"{avg:.0f} ms" if avg is not None else "—")
        self.quality.set("jitter", f"{jitter:.1f} ms" if jitter is not None else "—")
        if loss is None:
            self.quality.set("loss", "—")
        else:
            self.quality.set("loss", f"{loss * 100:.1f}%")
        self.quality.values["loss"].setStyleSheet(f"color: {theme.colors[loss_color(loss)]};")
        text, color = quality_verdict(avg, jitter, loss)
        if snap.get("outage_since"):
            text, color = "No connection — see the outage log below.", "bad"
        self.verdict.setText(text)
        self.verdict.setStyleSheet(f"color: {theme.colors[color]};")
        self.quality_chart.set_data(monitor.latency_history)
        self.method_label.setText(f"Measured with {monitor.probe_method} to {HOSTS[0]} every {PROBE_INTERVAL:.0f} s.")

        self.session.set("rx", fmt.data(monitor.session_rx))
        self.session.set("tx", fmt.data(monitor.session_tx))
        self.session.set("peak_down", fmt.speed(monitor.peak_down, unit))
        self.session.set("peak_up", fmt.speed(monitor.peak_up, unit))

        if snap.get("netinfo") is not None or self._details_tick == 0:
            self._update_link(monitor.netinfo)
            self._update_adapter(monitor.netinfo)
        self._details_tick += 1
        self._update_outages(snap)
