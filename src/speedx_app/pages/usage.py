import calendar
import datetime as dt

from PyQt5.QtWidgets import QButtonGroup, QGridLayout, QHBoxLayout, QPushButton, QWidget

from .. import formatting as fmt
from ..export import save_csv
from ..widgets.charts import BarChart, MeterBar
from ..widgets.common import Card, Legend, Page, label


class _UsageTile(Card):
    def __init__(self, title, parent=None):
        super().__init__(padding=16, spacing=4, parent=parent)
        self.body.addWidget(label(title, "Label"))
        self.value = label("—", "BigValue")
        self.body.addWidget(self.value)
        self.detail = label("", "Faint")
        self.body.addWidget(self.detail)

    def set(self, rx, tx):
        self.value.setText(fmt.data(rx + tx))
        self.detail.setText(f"↓ {fmt.data(rx)}   ↑ {fmt.data(tx)}")


def _next_cycle(start):
    year, month = (start.year + 1, 1) if start.month == 12 else (start.year, start.month + 1)
    return start.replace(year=year, month=month, day=min(start.day, calendar.monthrange(year, month)[1]))


class UsagePage(Page):
    def __init__(self, ctx):
        super().__init__("Data Usage", "How much internet data you use, tracked on this device")
        self.ctx = ctx
        self.range_days = 30

        self.today = _UsageTile("Today")
        self.yesterday = _UsageTile("Yesterday")
        self.cycle = _UsageTile("This month")
        self.session = _UsageTile("This session")
        tiles = QGridLayout()
        tiles.setSpacing(16)
        for i, t in enumerate((self.today, self.yesterday, self.cycle, self.session)):
            tiles.addWidget(t, 0, i)
        self.add_layout(tiles)

        # monthly limit
        self.limit_card = Card("Monthly data limit")
        self.limit_bar = MeterBar("accent", 12)
        self.limit_text = label("", "Muted", wrap=True)
        self.limit_card.add(self.limit_bar)
        self.limit_card.add(self.limit_text)
        self.add(self.limit_card)

        # chart with range selector
        seg = QWidget()
        seg_lay = QHBoxLayout(seg)
        seg_lay.setContentsMargins(0, 0, 0, 0)
        seg_lay.setSpacing(0)
        self.range_group = QButtonGroup(self)
        for days in (7, 30, 90):
            b = QPushButton(f"{days} days")
            b.setObjectName("Segment")
            b.setCheckable(True)
            b.setChecked(days == self.range_days)
            b.setProperty("segment", {7: "first", 90: "last"}.get(days, "mid"))
            self.range_group.addButton(b, days)
            seg_lay.addWidget(b)
        self.range_group.buttonClicked[int].connect(self._set_range)
        self.chart = BarChart([("Download", "down"), ("Upload", "up")], formatter=fmt.data)
        self.chart.setMinimumHeight(280)
        head = QHBoxLayout()
        head.addWidget(Legend([("Download", "down"), ("Upload", "up")]))
        head.addStretch(1)
        head.addWidget(seg)
        self.export_btn = QPushButton("Export CSV")
        self.export_btn.setObjectName("Link")
        self.export_btn.clicked.connect(self._export)
        chart_card = Card("Daily usage", "Hover a bar for details", trailing=self.export_btn)
        chart_card.add_layout(head)
        chart_card.add(self.chart, 1)
        self.add(chart_card)
        self.range_total = label("", "Muted")
        self.recovered_note = label("", "Faint", wrap=True)
        self.add(self.recovered_note)
        self.add(label("SpeedX counts traffic on physical network adapters (Wi-Fi, Ethernet, USB tethering, "
                       "mobile modems). Container, bridge and VPN interfaces are left out because their traffic "
                       "also passes through a physical adapter and would be counted twice. Usage while SpeedX is "
                       "closed is filled in the next time it starts.", "Faint", wrap=True))
        chart_card.add(self.range_total)
        self.finish()
        self._tick = 0

    def _export(self):
        rows = [[day, rx, tx, rx + tx, round(rx / 1e6, 2), round(tx / 1e6, 2), round((rx + tx) / 1e6, 2)]
                for day, (rx, tx) in sorted(self.ctx.usage.days.items())]
        save_csv(self, "speedx-data-usage",
                 ["date", "downloaded_bytes", "uploaded_bytes", "total_bytes", "downloaded_mb", "uploaded_mb",
                  "total_mb"], rows, self.export_btn)

    def _set_range(self, days):
        self.range_days = days
        self._refresh_chart()

    def _refresh_chart(self):
        days = self.ctx.usage.last_days(self.range_days)
        fmt_label = "%a" if self.range_days <= 7 else "%d %b"
        self.chart.set_bars([(d.strftime(fmt_label), [rx, tx]) for d, rx, tx in days])
        rx = sum(r for _, r, _ in days)
        tx = sum(t for _, _, t in days)
        avg = (rx + tx) / max(1, len(days))
        self.range_total.setText(f"Total {fmt.data(rx + tx)}  ·  ↓ {fmt.data(rx)}  ↑ {fmt.data(tx)}  ·  "
                                 f"Average {fmt.data(avg)} per day")

    def on_shown(self):
        self._tick = 0

    def on_snapshot(self, snap, monitor):
        usage = self.ctx.usage
        cfg = self.ctx.config
        today = dt.date.today()
        self.today.set(*usage.day(today))
        self.yesterday.set(*usage.day(today - dt.timedelta(days=1)))
        rx, tx = usage.cycle_total(cfg.get("billing_day"))
        self.cycle.set(rx, tx)
        self.session.set(monitor.session_rx, monitor.session_tx)
        recovered = usage.recovered
        self.recovered_note.setText(f"Today includes {fmt.data(recovered)} used while SpeedX was not running."
                                    if recovered else "")
        self.recovered_note.setVisible(bool(recovered))

        start = usage.cycle_start(cfg.get("billing_day"))
        reset = _next_cycle(start)
        limit_gb = cfg.get("data_limit_gb")
        if limit_gb > 0:
            limit = limit_gb * 1e9
            used = rx + tx
            frac = used / limit
            color = "bad" if frac >= 1 else "warn" if frac >= 0.8 else "accent"
            self.limit_bar.set_fraction(frac, color)
            days_left = (reset - today).days
            if used >= limit:
                text = f"Limit exceeded by {fmt.data(used - limit)}."
            else:
                text = f"{fmt.data(limit - used)} left of {limit_gb:g} GB."
            self.limit_text.setText(f"{text}  Resets on {reset.strftime('%d %b')} ({days_left} days).")
            self.limit_card.title_label.setText(f"Monthly data limit · {frac * 100:.0f}% used")
        else:
            self.limit_bar.set_fraction(0)
            self.limit_card.title_label.setText("Monthly data limit")
            self.limit_text.setText("No limit set. On a metered or capped connection, set a monthly limit in "
                                    f"Settings to get a warning before you run out. Cycle started {start.strftime('%d %b')}.")

        if self._tick % 5 == 0:
            self._refresh_chart()
        self._tick += 1
