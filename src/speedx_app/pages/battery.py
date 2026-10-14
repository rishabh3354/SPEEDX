from .. import formatting as fmt
from ..battery import status_text
from ..widgets.charts import LineChart, MeterBar, RingGauge
from ..widgets.common import Card, InfoGrid, Page, label, row


def battery_color(percent, status):
    if status == "Charging":
        return "good"
    if percent is None:
        return "muted"
    return "bad" if percent <= 15 else "warn" if percent <= 30 else "good"


def health_text(health):
    if health is None:
        return "—", "muted"
    if health >= 80:
        return f"{health:.0f}%  ·  Good", "good"
    if health >= 60:
        return f"{health:.0f}%  ·  Worn", "warn"
    return f"{health:.0f}%  ·  Consider replacing", "bad"


class BatteryPage(Page):
    def __init__(self, ctx):
        super().__init__("Battery", "Charge, power draw and battery health")
        self.ctx = ctx

        self.ring = RingGauge("good", thickness=14)
        self.ring.setMinimumSize(190, 190)
        ring_card = Card("Charge")
        ring_card.add(self.ring, 1)
        self.status = label("", "Muted", wrap=True)
        ring_card.add(self.status)

        self.info = InfoGrid([
            ("status", "Status"), ("time", "Time remaining"), ("power", "Power draw"),
            ("energy", "Energy"), ("voltage", "Voltage"),
        ])
        now_card = Card("Right now")
        now_card.add(self.info)
        now_card.body.addStretch(1)
        self.add_layout(row(ring_card, now_card, stretches=[1, 2]))

        self.health_bar = MeterBar("good", 10)
        self.health = InfoGrid([
            ("health", "Health"), ("capacity", "Full capacity"), ("design", "Design capacity"),
            ("cycles", "Charge cycles"), ("tech", "Technology"), ("model", "Battery"),
        ], columns=2)
        self.health_tip = label("", "Faint", wrap=True)
        health_card = Card("Health", "How much of its original capacity the battery still holds")
        health_card.add(self.health_bar)
        health_card.add(self.health)
        health_card.add(self.health_tip)
        self.add(health_card)

        self.chart = LineChart([("Power", "warn")], min_y_max=10, formatter=lambda v: f"{v:.1f} W")
        self.chart.setMinimumHeight(200)
        chart_card = Card("Power draw", "Last 2 minutes · longer history is on the History page")
        chart_card.add(self.chart, 1)
        self.add(chart_card)
        self.finish()

    def on_snapshot(self, snap, monitor):
        b = snap.get("battery")
        if not b:
            self.status.setText("No battery detected.")
            return
        pct, status = b.get("percent"), b.get("status")
        color = battery_color(pct, status)
        self.ring.color_key = color
        short = {"Charging": "charging", "Discharging": "on battery", "Not charging": "not charging",
                 "Full": "full"}.get(status, "")
        self.ring.set_value(pct or 0, f"{pct:.0f}%" if pct is not None else "—", short)

        friendly = status_text(b)
        tip = ""
        if "charge limit" in friendly:
            tip = ("Charging stops below 100% to extend battery life. This is a battery protection setting "
                   "(firmware or system), not a problem.")
        elif status == "Discharging" and pct is not None and pct <= 20:
            tip = "Battery is low. Plug in soon."
        self.status.setText(tip)
        self.status.setVisible(bool(tip))

        self.info.set("status", friendly)
        left = b.get("time_left")
        if left:
            self.info.set("time", f"{fmt.duration_precise(left)} until {'full' if status == 'Charging' else 'empty'}")
        else:
            self.info.set("time", "—")
        power = b.get("power")
        if power is None:
            self.info.set("power", "—")
        elif power < 0.05:
            self.info.set("power", "0 W (running on AC power)" if b.get("plugged") else "0 W")
        else:
            verb = "charging at" if status == "Charging" else "using"
            self.info.set("power", f"{verb} {power:.1f} W")
        now, full, design = b.get("energy_now"), b.get("energy_full"), b.get("energy_design")
        self.info.set("energy", f"{now:.1f} of {full:.1f} Wh" if now and full else "—")
        self.info.set("voltage", f"{b['voltage']:.2f} V" if b.get("voltage") else "—")

        text, hcolor = health_text(b.get("health"))
        self.health.set("health", text)
        self.health.values["health"].setStyleSheet("")
        self.health_bar.set_fraction((b.get("health") or 0) / 100, hcolor)
        self.health.set("capacity", f"{full:.1f} Wh" if full else "—")
        self.health.set("design", f"{design:.1f} Wh" if design else "—")
        self.health.set("cycles", str(b["cycles"]) if b.get("cycles") else "—")
        self.health.set("tech", b.get("technology") or "—")
        maker = " ".join(x for x in (b.get("manufacturer"), b.get("model")) if x)
        self.health.set("model", maker or "—")
        if b.get("health") is not None:
            lost = 100 - b["health"]
            self.health_tip.setText(f"Your battery has lost about {lost:.0f}% of its original capacity"
                                    + (f" after {b['cycles']} charge cycles." if b.get("cycles") else ".")
                                    + " Most laptop batteries are considered worn below 80%.")
        self.chart.set_data(monitor.history["power"], capacity=monitor.history["power"].maxlen)
