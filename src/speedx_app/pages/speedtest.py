import datetime as dt
import statistics
import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAbstractItemView, QButtonGroup, QGridLayout, QHBoxLayout, QHeaderView, QPushButton,
                             QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from .. import formatting as fmt
from ..export import save_csv
from ..speedtest import SpeedTest
from ..widgets.charts import SpeedGauge, TimeSeriesChart
from ..widgets.common import Card, IconLabel, Legend, Page, label, row

PHASE_COLORS = {"latency": "accent", "download": "down", "upload": "up"}
PHASE_TEXT = {"latency": "Measuring latency…", "download": "Testing download…", "upload": "Testing upload…"}
CHART_RANGES = [("7 days", 7 * 86400), ("30 days", 30 * 86400), ("90 days", 90 * 86400), ("All", None)]
MAX_TABLE_ROWS = 100


class _ResultTile(QWidget):
    def __init__(self, title, icon_name, color_key, unit, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)
        head = QHBoxLayout()
        head.setSpacing(6)
        head.addWidget(IconLabel(icon_name, color_key, 16))
        head.addWidget(label(title, "Label"), 1)
        lay.addLayout(head)
        values = QHBoxLayout()
        values.setSpacing(6)
        self.value = label("–", "BigValue")
        values.addWidget(self.value)
        values.addWidget(label(unit, "Unit"), 0, Qt.AlignBottom)
        values.addStretch(1)
        lay.addLayout(values)

    def set(self, text):
        self.value.setText(text)


def _mbps(value):
    return f"{value:.1f}" if value < 100 else f"{value:.0f}"


def _timestamp(result):
    try:
        return dt.datetime.fromisoformat(result["time"]).timestamp()
    except (KeyError, ValueError):
        return None


def verdict(res):
    d, ping = res["download"], res["ping"]
    if d >= 100 and ping < 40:
        text = "Excellent — great for 4K streaming, large downloads, video calls and online gaming."
    elif d >= 25:
        text = "Good — handles HD/4K streaming and video calls on several devices."
    elif d >= 8:
        text = "Fair — fine for browsing, HD streaming and calls on one or two devices."
    else:
        text = "Slow — browsing works, but streaming and calls may buffer."
    if ping >= 100:
        text += " High latency may cause lag in games and calls."
    return text


class SpeedTestPage(Page):
    CHART_HINT_OFF = "Turn on automatic tests in Settings to track your ISP over time"
    CHART_HINT_ON = "Manual and automatic tests · hover a point for details"

    def __init__(self, ctx):
        super().__init__("Speed Test", "Measure your real internet download, upload and latency")
        self.ctx = ctx
        self.test = None
        self.chart_range = 30 * 86400

        self.gauge = SpeedGauge()
        self.gauge.setMinimumSize(340, 320)
        self.start_btn = QPushButton("Start test")
        self.start_btn.setObjectName("Primary")
        self.start_btn.setMinimumWidth(180)
        self.start_btn.setMinimumHeight(40)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.clicked.connect(self.toggle)
        self.server = label("Server: Cloudflare (nearest location)", "Faint")
        self.server.setAlignment(Qt.AlignCenter)
        self.auto_status = label("", "Faint", wrap=True)
        self.auto_status.setAlignment(Qt.AlignCenter)

        gauge_card = Card()
        gauge_card.add(self.gauge, 1)
        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        btn_row.addWidget(self.start_btn)
        btn_row.addStretch(1)
        gauge_card.add_layout(btn_row)
        gauge_card.add(self.server)
        gauge_card.add(self.auto_status)

        self.ping = _ResultTile("Ping", "ping", "accent", "ms")
        self.jitter = _ResultTile("Jitter", "ping", "muted", "ms")
        self.down = _ResultTile("Download", "down", "down", "Mbps")
        self.up = _ResultTile("Upload", "up", "up", "Mbps")
        results = Card("Results")
        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(22)
        grid.addWidget(self.down, 0, 0)
        grid.addWidget(self.up, 0, 1)
        grid.addWidget(self.ping, 1, 0)
        grid.addWidget(self.jitter, 1, 1)
        results.add_layout(grid)
        self.verdict = label("Run a test to see what your connection can handle.", "Muted", wrap=True)
        results.add(self.verdict)
        results.body.addStretch(1)
        self.ip_label = label("", "Faint", wrap=True)
        results.add(self.ip_label)
        self.add_layout(row(gauge_card, results, stretches=[3, 2]))

        # results over time
        seg = QWidget()
        seg_lay = QHBoxLayout(seg)
        seg_lay.setContentsMargins(0, 0, 0, 0)
        seg_lay.setSpacing(0)
        self.range_group = QButtonGroup(self)
        for i, (text, seconds) in enumerate(CHART_RANGES):
            b = QPushButton(text)
            b.setObjectName("Segment")
            b.setCheckable(True)
            b.setChecked(seconds == self.chart_range)
            b.setProperty("segment", "first" if i == 0 else "last" if i == len(CHART_RANGES) - 1 else "mid")
            self.range_group.addButton(b, i)
            seg_lay.addWidget(b)
        self.range_group.buttonClicked[int].connect(self._set_chart_range)
        self.chart = TimeSeriesChart([("Download", "down"), ("Upload", "up")], formatter=lambda v: f"{v:.0f} Mbps",
                                     min_y_max=10, markers=True)
        self.chart.empty_text = "No speed tests in this period yet"
        self.chart.setMinimumHeight(230)
        head = QHBoxLayout()
        head.addWidget(Legend([("Download", "down"), ("Upload", "up")]))
        head.addStretch(1)
        head.addWidget(seg)
        self.chart_card = chart_card = Card("Speed over time", self.CHART_HINT_OFF)
        chart_card.add_layout(head)
        chart_card.add(self.chart, 1)
        self.chart_stats = label("", "Faint", wrap=True)
        chart_card.add(self.chart_stats)
        self.add(chart_card)

        # history table
        buttons = QWidget()
        b_lay = QHBoxLayout(buttons)
        b_lay.setContentsMargins(0, 0, 0, 0)
        b_lay.setSpacing(4)
        self.export_btn = QPushButton("Export CSV")
        self.export_btn.setObjectName("Link")
        self.export_btn.clicked.connect(self._export)
        clear = QPushButton("Clear history")
        clear.setObjectName("Link")
        clear.clicked.connect(self._clear_history)
        b_lay.addWidget(self.export_btn)
        b_lay.addWidget(clear)
        hist_card = Card("History", "Your previous speed tests", trailing=buttons)
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(["Date", "Type", "Download", "Upload", "Ping", "Jitter", "Server",
                                              "Data used"])
        self.table.verticalHeader().hide()
        self.table.setShowGrid(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.table.verticalHeader().setDefaultSectionSize(36)
        hist_card.add(self.table)
        self.empty_history = label("No tests yet.", "Muted")
        hist_card.add(self.empty_history)
        self.add(hist_card)
        self.finish()
        self._load_history()

    # --------------------------------------------------------------- history
    def _load_history(self):
        results = self.ctx.speed_history.results
        shown = results[:MAX_TABLE_ROWS]
        self.table.setRowCount(len(shown))
        for r, res in enumerate(shown):
            ts = _timestamp(res)
            if ts:
                stamp = dt.datetime.fromtimestamp(ts)
                when = stamp.strftime("%d %b, %H:%M" if stamp.year == dt.date.today().year else "%d %b %Y, %H:%M")
            else:
                when = res.get("time", "")
            server = " · ".join(x for x in (res.get("server"), res.get("location")) if x)
            used = res.get("data_used")
            cells = [when, "Automatic" if res.get("automatic") else "Manual",
                     f"{_mbps(res['download'])} Mbps", f"{_mbps(res['upload'])} Mbps",
                     f"{res['ping']:.0f} ms", f"{res.get('jitter', 0):.0f} ms", server or "—",
                     fmt.data(used) if used else "—"]
            for c, text in enumerate(cells):
                self.table.setItem(r, c, QTableWidgetItem(text))
        header = self.table.horizontalHeader().sizeHint().height()
        self.table.setFixedHeight(header + min(len(shown), 10) * self.table.verticalHeader().defaultSectionSize() + 4)
        self.table.setVisible(bool(results))
        self.empty_history.setVisible(not results)
        self.export_btn.setEnabled(bool(results))
        if results and not self.is_running():
            last = results[0]
            self.down.set(_mbps(last["download"]))
            self.up.set(_mbps(last["upload"]))
            self.ping.set(f"{last['ping']:.0f}")
            self.jitter.set(f"{last.get('jitter', 0):.0f}")
            self.verdict.setText(verdict(last))
        self._refresh_chart()

    def _set_chart_range(self, index):
        self.chart_range = CHART_RANGES[index][1]
        self._refresh_chart()

    def _refresh_chart(self):
        now = time.time()
        points = [(ts, r) for r in self.ctx.speed_history.results for ts in [_timestamp(r)] if ts]
        if self.chart_range:
            start = now - self.chart_range
        else:
            start = min((ts for ts, _ in points), default=now - 86400) - 3600
        points = sorted(((ts, r) for ts, r in points if ts >= start), key=lambda p: p[0])
        self.chart.set_data([[(ts, r["download"]) for ts, r in points], [(ts, r["upload"]) for ts, r in points]],
                            start, now, 3600)
        if points:
            downs = [r["download"] for _, r in points]
            ups = [r["upload"] for _, r in points]
            pings = [r["ping"] for _, r in points]
            self.chart_stats.setText(
                f"{len(points)} test{'s' if len(points) != 1 else ''}  ·  Typical ↓ {_mbps(statistics.median(downs))}"
                f" Mbps  ↑ {_mbps(statistics.median(ups))} Mbps  ·  Ping {statistics.median(pings):.0f} ms  ·  "
                f"Slowest ↓ {_mbps(min(downs))} Mbps")
        else:
            self.chart_stats.setText("")

    def _clear_history(self):
        self.ctx.speed_history.clear()
        self._load_history()

    def _export(self):
        rows = []
        for res in self.ctx.speed_history.results:
            rows.append([res.get("time", ""), "automatic" if res.get("automatic") else "manual",
                         res.get("download"), res.get("upload"), res.get("ping"), res.get("jitter"),
                         res.get("provider", "Cloudflare"), res.get("server", ""), res.get("location", ""),
                         round(res["data_used"] / 1e6, 1) if res.get("data_used") else ""])
        save_csv(self, "speedx-speed-tests",
                 ["time", "type", "download_mbps", "upload_mbps", "ping_ms", "jitter_ms", "provider", "server",
                  "location", "data_used_mb"], rows, self.export_btn)

    # ------------------------------------------------------------------ test
    def is_running(self):
        return bool(self.test and self.test.isRunning())

    def toggle(self):
        if self.is_running():
            self.test.cancel()
            self.start_btn.setEnabled(False)
            self.start_btn.setText("Stopping…")
            return
        self.start_test(automatic=False)

    def start_test(self, automatic=False):
        if self.is_running():
            return False
        for tile in (self.ping, self.jitter, self.down, self.up):
            tile.set("–")
        self.verdict.setText("Automatic test running…" if automatic else
                             "Testing… keep other downloads paused for the most accurate result.")
        self.ip_label.setText("")
        self.gauge.set_state(0, "accent", "Connecting…", "0")
        self.start_btn.setText("Stop")
        self.test = SpeedTest(profile="light" if automatic else "full", automatic=automatic, parent=self)
        self.test.progress.connect(self._on_progress)
        self.test.phase_done.connect(self._on_phase_done)
        self.test.server_info.connect(self._on_server)
        self.test.completed.connect(self._on_completed)
        self.test.failed.connect(self._on_failed)
        self.test.finished.connect(self._on_finished)
        self.test.start()
        return True

    def _on_server(self, info):
        name = info.get("server") or info.get("provider", "")
        where = f" · {info['location']}" if info.get("location") else ""
        self.server.setText(f"Server: {name}{where}")
        if info.get("ip"):
            self.ip_label.setText(f"Public IP: {info['ip']}")

    def _on_progress(self, phase, value, fraction):
        color = PHASE_COLORS[phase]
        if phase == "latency":
            self.gauge.set_state(0, color, PHASE_TEXT[phase], f"{value:.0f}", unit="ms")
        else:
            self.gauge.set_state(value, color, PHASE_TEXT[phase])

    def _on_phase_done(self, phase, value):
        if phase == "latency":
            self.ping.set(f"{value:.0f}")
        elif phase == "download":
            self.down.set(_mbps(value))
        elif phase == "upload":
            self.up.set(_mbps(value))

    def _on_completed(self, result):
        previous = [r["download"] for r in self.ctx.speed_history.results[:20]]
        self.jitter.set(f"{result['jitter']:.0f}")
        self.gauge.set_state(result["download"], "down", "Test complete", _mbps(result["download"]))
        self.verdict.setText(verdict(result))
        self.ctx.speed_history.add(result)
        self._load_history()
        self.ctx.on_speed_test_result(result, previous)

    def _on_failed(self, message):
        if message == "cancelled":
            self.gauge.set_state(0, "muted", "Test cancelled", "0")
            self.verdict.setText("Test cancelled.")
        else:
            self.gauge.set_state(0, "bad", "Test failed", "—", unit="")
            self.verdict.setText(f"Could not complete the test: {message}. Check your connection and try again.")

    def _on_finished(self):
        self.start_btn.setEnabled(True)
        self.start_btn.setText("Test again")

    def set_auto_status(self, text):
        self.auto_status.setText(text)
        self.auto_status.setVisible(bool(text))
        self.chart_card.hint_label.setText(self.CHART_HINT_ON if text else self.CHART_HINT_OFF)

    def shutdown(self):
        if self.is_running():
            self.test.cancel()
            self.test.wait(3000)
