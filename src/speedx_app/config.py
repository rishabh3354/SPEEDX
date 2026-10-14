"""Typed application settings stored with QSettings."""

import os

from PyQt5.QtCore import QObject, QSettings, QStandardPaths, pyqtSignal

from . import APP_ID, ORG_NAME

DEFAULTS = {
    "theme": "dark",                # dark | light | system
    "interval": 1.0,                # seconds between samples
    "speed_unit": "bytes",          # bytes | bits
    "temp_unit": "C",               # C | F
    "interface": "",                # "" = all interfaces
    "close_to_tray": True,
    "tray_speed": True,             # live speed in the tray / top bar
    "tray_content": "both",         # both | down | total | all
    "tray_style": "auto",           # auto | label | icon
    "start_minimized": False,
    "group_processes": True,
    "autostart": False,
    "mini_meter": False,
    "mini_meter_stats": True,       # show CPU / RAM in the mini meter
    "mini_meter_pos": None,
    "alerts_enabled": True,
    "alert_cpu": 90,
    "alert_ram": 90,
    "alert_temp": 85,
    "alert_connection": True,       # notify when the internet drops / returns
    "alert_slow_speed": True,       # notify when an automatic test is far below normal
    "auto_test_hours": 0,           # automatic speed test interval (0 = off)
    "data_limit_gb": 0.0,           # 0 = no monthly limit
    "billing_day": 1,
    "window_geometry": None,
}


class Config(QObject):
    changed = pyqtSignal(str, object)

    def __init__(self):
        super().__init__()
        self._qs = QSettings(ORG_NAME, APP_ID)
        self._cache = {}
        for key, default in DEFAULTS.items():
            self._cache[key] = self._read(key, default)

    def _read(self, key, default):
        if not self._qs.contains(key):
            return default
        value = self._qs.value(key)
        try:
            if isinstance(default, bool):
                return value in (True, "true", "1", 1)
            if isinstance(default, int):
                return int(float(value))
            if isinstance(default, float):
                return float(value)
            if isinstance(default, str):
                return str(value)
        except (TypeError, ValueError):
            return default
        return value

    def get(self, key):
        return self._cache.get(key, DEFAULTS.get(key))

    def set(self, key, value):
        if self._cache.get(key) == value:
            return
        self._cache[key] = value
        self._qs.setValue(key, value)
        self.changed.emit(key, value)

    def sync(self):
        self._qs.sync()


def data_dir():
    path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    if not path:
        path = os.path.join(os.path.expanduser("~"), ".local", "share", APP_ID)
    os.makedirs(path, exist_ok=True)
    return path
