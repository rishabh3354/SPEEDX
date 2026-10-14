"""Details about the active network link (Wi-Fi signal, band, link rate).

NetworkManager is queried over the system D-Bus (via jeepney) when available;
otherwise /proc/net/wireless and sysfs provide a reduced view.
"""

import os
import time

import psutil

from . import system

try:
    from jeepney import DBusAddress, Properties
    from jeepney.io.blocking import open_dbus_connection
except ImportError:  # jeepney is optional
    open_dbus_connection = None

NM = "org.freedesktop.NetworkManager"
NM_RETRY = 60.0


def _dbm_from_proc(iface):
    try:
        with open("/proc/net/wireless") as fh:
            for line in fh.readlines()[2:]:
                name, rest = line.split(":", 1)
                if name.strip() == iface:
                    level = float(rest.split()[2].rstrip("."))
                    return level if level < 0 else None
    except (OSError, ValueError, IndexError):
        pass
    return None


def _is_wireless(iface):
    return os.path.isdir(f"/sys/class/net/{iface}/wireless")


def band_and_channel(freq_mhz):
    if not freq_mhz:
        return None, None
    if 2400 <= freq_mhz < 2500:
        return "2.4 GHz", 14 if freq_mhz == 2484 else (freq_mhz - 2407) // 5
    if 5000 <= freq_mhz < 5925:
        return "5 GHz", (freq_mhz - 5000) // 5
    if 5925 <= freq_mhz < 7125:
        return "6 GHz", (freq_mhz - 5950) // 5
    return f"{freq_mhz / 1000:.1f} GHz", None


def signal_quality(dbm=None, percent=None):
    """('Excellent' | 'Good' | 'Fair' | 'Weak', color key)."""
    if dbm is not None:
        score = 3 if dbm >= -55 else 2 if dbm >= -67 else 1 if dbm >= -75 else 0
    elif percent is not None:
        score = 3 if percent >= 70 else 2 if percent >= 50 else 1 if percent >= 30 else 0
    else:
        return None, "muted"
    return [("Weak", "bad"), ("Fair", "warn"), ("Good", "good"), ("Excellent", "good")][score]


class NetworkInfo:
    def __init__(self):
        self._conn = None
        self._nm_failed_at = None

    def _nm(self):
        if open_dbus_connection is None:
            return None
        if self._conn is None:
            if self._nm_failed_at and time.monotonic() - self._nm_failed_at < NM_RETRY:
                return None
            try:
                self._conn = open_dbus_connection("SYSTEM")
            except Exception:  # noqa: BLE001 - no system bus / not permitted
                self._nm_failed_at = time.monotonic()
                return None
        return self._conn

    def _get(self, path, iface, prop):
        msg = Properties(DBusAddress(path, bus_name=NM, interface=iface)).get(prop)
        reply = self._conn.send_and_get_reply(msg, timeout=1.0)
        if reply.header.message_type.name != "method_return":
            raise LookupError(prop)
        return reply.body[0][1]

    def _from_networkmanager(self):
        if self._nm() is None:
            return None
        try:
            active = self._get("/org/freedesktop/NetworkManager", NM, "PrimaryConnection")
            if active in ("/", ""):
                return {"type": None}
            conn_type = self._get(active, NM + ".Connection.Active", "Type")
            name = self._get(active, NM + ".Connection.Active", "Id")
            devices = self._get(active, NM + ".Connection.Active", "Devices")
            info = {"type": "other", "name": name, "iface": None}
            if not devices:
                return info
            dev = devices[0]
            info["iface"] = self._get(dev, NM + ".Device", "Interface")
            # NMMetered: 1 = yes, 3 = guessed yes (e.g. phone hotspot), 2/4 = no, 0 = unknown
            info["metered"] = self._get(dev, NM + ".Device", "Metered") in (1, 3)
            if conn_type == "802-11-wireless":
                info["type"] = "wifi"
                info["bitrate"] = self._get(dev, NM + ".Device.Wireless", "Bitrate") / 1000.0
                ap = self._get(dev, NM + ".Device.Wireless", "ActiveAccessPoint")
                if ap not in ("/", ""):
                    ssid = self._get(ap, NM + ".AccessPoint", "Ssid")
                    info["ssid"] = bytes(ssid).decode("utf-8", "replace") if ssid else name
                    info["signal_pct"] = int(self._get(ap, NM + ".AccessPoint", "Strength"))
                    info["freq"] = int(self._get(ap, NM + ".AccessPoint", "Frequency"))
                    info["max_bitrate"] = self._get(ap, NM + ".AccessPoint", "MaxBitrate") / 1000.0
            elif conn_type == "802-3-ethernet":
                info["type"] = "ethernet"
                info["bitrate"] = float(self._get(dev, NM + ".Device.Wired", "Speed"))
            return info
        except Exception:  # noqa: BLE001 - NM missing, denied or changed: fall back
            try:
                self._conn.close()
            except Exception:  # noqa: BLE001
                pass
            self._conn = None
            self._nm_failed_at = time.monotonic()
            return None

    def _from_kernel(self):
        ip = system.local_ip()
        if not ip:
            return {"type": None}
        iface = next((d["name"] for d in system.interface_details() if d["ipv4"] == ip), None)
        if not iface:
            return {"type": "other", "iface": None}
        if _is_wireless(iface):
            return {"type": "wifi", "iface": iface, "ssid": None}
        speed = psutil.net_if_stats().get(iface)
        return {"type": "ethernet" if iface.startswith(("en", "eth")) else "other", "iface": iface,
                "bitrate": float(speed.speed) if speed and speed.speed else None}

    def query(self):
        info = self._from_networkmanager() or self._from_kernel()
        if info.get("type") == "wifi" and info.get("iface"):
            info["signal_dbm"] = _dbm_from_proc(info["iface"])
            info["band"], info["channel"] = band_and_channel(info.get("freq"))
        return info
