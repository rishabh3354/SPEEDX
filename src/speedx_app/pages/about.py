from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from .. import APP_NAME, DONATE_URL, FEEDBACK_URL, SNAP_STORE_URL, VERSION, WEBSITE_URL
from ..widgets.common import Card, InfoGrid, Page, label

FEATURES = [
    "Live CPU, memory, disk and network monitoring with history graphs",
    "Real internet speed test with ping, jitter and saved history",
    "Daily and monthly data usage tracking with a data cap warning",
    "Process manager to find and stop heavy applications",
    "Always-on-top mini meter, system tray and desktop alerts",
]


class AboutPage(Page):
    def __init__(self, ctx, icon_path):
        super().__init__("About", "")
        self.ctx = ctx

        hero = Card(padding=26)
        top = QHBoxLayout()
        top.setSpacing(20)
        logo = QLabel()
        pm = QPixmap(icon_path)
        if not pm.isNull():
            logo.setPixmap(pm.scaled(84, 84, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        top.addWidget(logo, 0, Qt.AlignTop)
        texts = QVBoxLayout()
        texts.setSpacing(4)
        texts.addWidget(label(APP_NAME, "BigValue"))
        texts.addWidget(label(f"Version {VERSION}", "Muted"))
        texts.addWidget(label("A fast, lightweight system and internet monitor for Linux.", "Muted", wrap=True))
        texts.addStretch(1)
        top.addLayout(texts, 1)
        hero.add_layout(top)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        for text, url, primary in (("Rate on Snap Store", SNAP_STORE_URL, True), ("Send feedback", FEEDBACK_URL, False),
                                   ("More apps", WEBSITE_URL, False), ("Donate", DONATE_URL, False)):
            b = QPushButton(text)
            if primary:
                b.setObjectName("Primary")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _, u=url: QDesktopServices.openUrl(QUrl(u)))
            buttons.addWidget(b)
        buttons.addStretch(1)
        hero.add_layout(buttons)
        self.add(hero)

        features = Card("What SpeedX does")
        for f in FEATURES:
            features.add(label("•  " + f, "Muted", wrap=True))
        self.add(features)

        info = ctx.monitor.info
        sysinfo = InfoGrid([("host", "Device"), ("os", "System"), ("kernel", "Kernel"), ("cpu", "Processor")])
        sysinfo.set("host", info["hostname"])
        sysinfo.set("os", info["os"])
        sysinfo.set("kernel", f"{info['kernel']} ({info['arch']})")
        sysinfo.set("cpu", info["cpu_model"])
        sys_card = Card("This computer")
        sys_card.add(sysinfo)
        self.add(sys_card)

        self.add(label("Tip: if CPU temperature shows “N/A” in the Snap version, run "
                       "“sudo snap connect speedx:hardware-observe”.", "Faint", wrap=True))
        self.add(label("Speed tests use Cloudflare's public speed test servers (speed.cloudflare.com).",
                       "Faint", wrap=True))
        self.finish()
