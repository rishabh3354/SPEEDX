"""Laptop battery details from /sys/class/power_supply (no privileges needed)."""

import os

import psutil

SYS = "/sys/class/power_supply"


def _read(path, name, cast=str):
    try:
        with open(os.path.join(path, name)) as fh:
            value = fh.read().strip()
        return cast(value) if value != "" else None
    except (OSError, ValueError):
        return None


def _battery_path():
    try:
        names = sorted(os.listdir(SYS))
    except OSError:
        return None
    for name in names:
        path = os.path.join(SYS, name)
        # scope "Device" marks batteries of mice, keyboards, headsets...
        if _read(path, "type") == "Battery" and _read(path, "scope") != "Device" \
                and _read(path, "present", int) != 0:
            return path
    return None


def _on_ac():
    try:
        names = os.listdir(SYS)
    except OSError:
        return None
    states = [_read(os.path.join(SYS, n), "online", int) for n in names
              if _read(os.path.join(SYS, n), "type") in ("Mains", "USB")]
    states = [s for s in states if s is not None]
    return any(states) if states else None


def has_battery():
    return _battery_path() is not None or psutil.sensors_battery() is not None


def battery_info():
    """Dict describing the main battery, or None on desktops."""
    path = _battery_path()
    if path is None:
        fallback = psutil.sensors_battery()
        if fallback is None:
            return None
        return {"percent": fallback.percent, "status": "Discharging" if fallback.power_plugged is False else "Unknown",
                "plugged": fallback.power_plugged, "power": None, "health": None, "cycles": None,
                "time_left": fallback.secsleft if fallback.secsleft and fallback.secsleft > 0 else None}

    info = {
        "percent": _read(path, "capacity", float),
        "status": _read(path, "status") or "Unknown",
        "technology": _read(path, "technology"),
        "manufacturer": _read(path, "manufacturer"),
        "model": _read(path, "model_name"),
        "cycles": _read(path, "cycle_count", int) or None,
        "voltage": (_read(path, "voltage_now", int) or 0) / 1e6 or None,
        "charge_limit": _read(path, "charge_control_end_threshold", int),
        "plugged": _on_ac(),
    }

    # Batteries report either energy (µWh) or charge (µAh); normalise to Wh.
    volts_design = (_read(path, "voltage_min_design", int) or 0) / 1e6
    energy_now = _read(path, "energy_now", int)
    if energy_now is not None:
        now = energy_now / 1e6
        full = (_read(path, "energy_full", int) or 0) / 1e6
        design = (_read(path, "energy_full_design", int) or 0) / 1e6
    else:
        volts = volts_design or info["voltage"] or 0
        now = (_read(path, "charge_now", int) or 0) / 1e6 * volts
        full = (_read(path, "charge_full", int) or 0) / 1e6 * volts
        design = (_read(path, "charge_full_design", int) or 0) / 1e6 * volts
    info["energy_now"] = now or None
    info["energy_full"] = full or None
    info["energy_design"] = design or None
    info["health"] = min(100.0, full / design * 100) if full and design else None
    if info["percent"] is None and full:
        info["percent"] = min(100.0, now / full * 100)

    power = _read(path, "power_now", int)
    if power is not None:
        watts = abs(power) / 1e6
    else:
        current = _read(path, "current_now", int)
        watts = abs(current) * (info["voltage"] or volts_design) / 1e6 if current is not None else None
    info["power"] = watts if watts else (0.0 if watts == 0 else None)

    status = info["status"]
    info["time_left"] = None
    if watts and watts > 0.1 and now and full:
        if status == "Discharging":
            info["time_left"] = now / watts * 3600
        elif status == "Charging":
            info["time_left"] = max(0.0, full - now) / watts * 3600
    return info


def status_text(info):
    """Human friendly status, e.g. 'Charging', 'On battery', 'Charge limit reached'."""
    status = info.get("status")
    if status == "Discharging":
        return "On battery"
    if status == "Not charging":
        if info.get("plugged") and (info.get("percent") or 0) < 99:
            return "Plugged in, not charging (charge limit)"
        return "Plugged in, not charging"
    if status == "Full":
        return "Fully charged"
    return status or "Unknown"
