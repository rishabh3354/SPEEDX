"""Color palettes and the global Qt style sheet."""

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication

DARK = {
    "bg": "#0e1116",
    "sidebar": "#12161d",
    "surface": "#171b23",
    "surface2": "#1e232d",
    "hover": "#252b37",
    "border": "#262c38",
    "grid": "#222833",
    "text": "#e7eaf0",
    "muted": "#8a93a6",
    "faint": "#5d6577",
    "accent": "#5b8cff",
    "accent_text": "#ffffff",
    "cpu": "#5b8cff",
    "mem": "#c084fc",
    "down": "#2dd4bf",
    "up": "#f472b6",
    "disk": "#fbbf24",
    "good": "#34d399",
    "warn": "#fbbf24",
    "bad": "#f87171",
}

LIGHT = {
    "bg": "#f4f6f9",
    "sidebar": "#ffffff",
    "surface": "#ffffff",
    "surface2": "#f1f3f7",
    "hover": "#e9edf3",
    "border": "#e2e6ed",
    "grid": "#eceff4",
    "text": "#151922",
    "muted": "#5f6878",
    "faint": "#98a0af",
    "accent": "#3b6ef5",
    "accent_text": "#ffffff",
    "cpu": "#3b6ef5",
    "mem": "#9333ea",
    "down": "#0d9488",
    "up": "#db2777",
    "disk": "#d97706",
    "good": "#059669",
    "warn": "#d97706",
    "bad": "#dc2626",
}


class _Theme(QObject):
    changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.name = "dark"
        self.colors = dict(DARK)
        self._system_dark = True

    def detect_system(self):
        """Remember whether the desktop palette is dark (call before styling)."""
        app = QApplication.instance()
        if app:
            self._system_dark = app.palette().color(QPalette.Window).lightness() < 128

    def apply(self, name):
        self.name = name
        dark = self._system_dark if name == "system" else name != "light"
        self.colors = dict(DARK if dark else LIGHT)
        app = QApplication.instance()
        if app:
            app.setStyleSheet(build_stylesheet(self.colors))
            pal = app.palette()
            pal.setColor(QPalette.Window, QColor(self.colors["bg"]))
            pal.setColor(QPalette.WindowText, QColor(self.colors["text"]))
            pal.setColor(QPalette.Base, QColor(self.colors["surface"]))
            pal.setColor(QPalette.Text, QColor(self.colors["text"]))
            pal.setColor(QPalette.Highlight, QColor(self.colors["accent"]))
            pal.setColor(QPalette.HighlightedText, QColor(self.colors["accent_text"]))
            pal.setColor(QPalette.ToolTipBase, QColor(self.colors["surface2"]))
            pal.setColor(QPalette.ToolTipText, QColor(self.colors["text"]))
            app.setPalette(pal)
        self.changed.emit()

    def color(self, key, alpha=None):
        c = QColor(self.colors.get(key, key))
        if alpha is not None:
            c.setAlpha(alpha)
        return c

    @property
    def is_dark(self):
        return QColor(self.colors["bg"]).lightness() < 128


theme = _Theme()


def build_stylesheet(c):
    return f"""
* {{
    font-size: 10pt;
    color: {c['text']};
    outline: none;
}}
QMainWindow, #Root {{ background: {c['bg']}; }}
QToolTip {{
    background: {c['surface2']}; color: {c['text']};
    border: 1px solid {c['border']}; padding: 6px 8px; border-radius: 6px;
}}

/* ---------- sidebar ---------- */
#Sidebar {{ background: {c['sidebar']}; border-right: 1px solid {c['border']}; }}
#Brand {{ font-size: 15pt; font-weight: 700; }}
#BrandSub {{ color: {c['muted']}; font-size: 8.5pt; }}
#NavButton {{
    text-align: left; padding: 9px 12px; border: none; border-radius: 8px;
    background: transparent; color: {c['muted']}; font-weight: 500;
}}
#NavButton:hover {{ background: {c['hover']}; color: {c['text']}; }}
#NavButton:checked {{ background: {c['surface2']}; color: {c['text']}; font-weight: 600; }}
#NavSection {{ color: {c['faint']}; font-size: 8pt; font-weight: 600; padding: 10px 12px 4px 12px; }}
#StatusPill {{
    background: {c['surface2']}; border: 1px solid {c['border']}; border-radius: 10px;
}}

/* ---------- page chrome ---------- */
#PageTitle {{ font-size: 19pt; font-weight: 700; }}
#PageSubtitle {{ color: {c['muted']}; }}
QScrollArea, #PageBody {{ background: transparent; border: none; }}
QScrollBar:vertical {{ background: transparent; width: 10px; margin: 2px; }}
QScrollBar::handle:vertical {{ background: {c['border']}; border-radius: 4px; min-height: 30px; }}
QScrollBar::handle:vertical:hover {{ background: {c['faint']}; }}
QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 2px; }}
QScrollBar::handle:horizontal {{ background: {c['border']}; border-radius: 4px; min-width: 30px; }}
QScrollBar::add-line, QScrollBar::sub-line, QScrollBar::add-page, QScrollBar::sub-page {{
    background: none; border: none; width: 0; height: 0;
}}

/* ---------- cards ---------- */
#Card {{ background: {c['surface']}; border: 1px solid {c['border']}; border-radius: 14px; }}
#CardTitle {{ font-size: 10.5pt; font-weight: 600; }}
#CardHint {{ color: {c['muted']}; font-size: 9pt; }}
#Muted {{ color: {c['muted']}; }}
#Faint {{ color: {c['faint']}; font-size: 9pt; }}
#Label {{ color: {c['muted']}; font-size: 9pt; }}
#Value {{ font-size: 10.5pt; font-weight: 600; }}
#BigValue {{ font-size: 24pt; font-weight: 700; }}
#HugeValue {{ font-size: 40pt; font-weight: 700; }}
#Unit {{ color: {c['muted']}; font-size: 11pt; font-weight: 600; }}
#Divider {{ background: {c['border']}; max-height: 1px; min-height: 1px; border: none; }}
#Chip {{
    background: {c['surface2']}; border-radius: 9px; padding: 3px 9px;
    color: {c['muted']}; font-size: 8.5pt; font-weight: 600;
}}
#Banner {{
    background: {c['surface2']}; border: 1px solid {c['border']}; border-radius: 10px; padding: 10px 14px;
}}

/* ---------- inputs ---------- */
QPushButton {{
    background: {c['surface2']}; border: 1px solid {c['border']}; border-radius: 8px;
    padding: 7px 14px; font-weight: 600;
}}
QPushButton:hover {{ background: {c['hover']}; }}
QPushButton:disabled {{ color: {c['faint']}; }}
QPushButton#Primary {{ background: {c['accent']}; color: {c['accent_text']}; border: none; }}
QPushButton#Primary:hover {{ background: {c['accent']}; border: 2px solid {c['text']}; }}
QPushButton#Danger {{ color: {c['bad']}; }}
QPushButton#Link {{ background: transparent; border: none; color: {c['accent']}; padding: 4px; }}
QPushButton#Segment {{ border-radius: 0; border: 1px solid {c['border']}; padding: 6px 12px; }}
QPushButton#Segment[segment="first"] {{ border-top-left-radius: 8px; border-bottom-left-radius: 8px; }}
QPushButton#Segment[segment="last"] {{ border-top-right-radius: 8px; border-bottom-right-radius: 8px; }}
QPushButton#Segment:checked {{ background: {c['accent']}; color: {c['accent_text']}; border-color: {c['accent']}; }}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
    background: {c['surface2']}; border: 1px solid {c['border']}; border-radius: 8px;
    padding: 6px 10px; min-height: 18px; selection-background-color: {c['accent']};
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{ border-color: {c['accent']}; }}
QComboBox::drop-down {{ border: none; width: 22px; }}
QComboBox QAbstractItemView {{
    background: {c['surface']}; border: 1px solid {c['border']}; padding: 4px;
    selection-background-color: {c['hover']}; selection-color: {c['text']};
}}
QSpinBox::up-button, QSpinBox::down-button, QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    width: 0; border: none;
}}
QMenu {{
    background: {c['surface']}; border: 1px solid {c['border']}; border-radius: 8px; padding: 4px;
}}
QMenu::item {{ padding: 6px 18px; border-radius: 6px; }}
QMenu::item:selected {{ background: {c['hover']}; }}
QMenu::separator {{ height: 1px; background: {c['border']}; margin: 4px 6px; }}

/* ---------- tables ---------- */
QTableView {{
    background: {c['surface']}; border: none; gridline-color: transparent;
    selection-background-color: {c['hover']}; selection-color: {c['text']};
    alternate-background-color: {c['surface']};
}}
QTableView::item {{ padding: 4px 8px; border-bottom: 1px solid {c['grid']}; }}
QTreeView {{
    background: {c['surface']}; border: none; show-decoration-selected: 1;
    selection-background-color: {c['hover']}; selection-color: {c['text']};
}}
QTreeView::item {{ padding: 5px 4px; border-bottom: 1px solid {c['grid']}; }}
QTreeView::item:hover {{ background: {c['surface2']}; }}
QTreeView::item:selected {{ background: {c['hover']}; color: {c['text']}; }}
QHeaderView {{ background: transparent; }}
QHeaderView::section {{
    background: {c['surface']}; color: {c['muted']}; border: none;
    border-bottom: 1px solid {c['border']}; padding: 8px; font-weight: 600; font-size: 9pt;
}}
QHeaderView::section:hover {{ color: {c['text']}; }}
QTableCornerButton::section {{ background: {c['surface']}; border: none; }}
"""
