"""Human readable formatting helpers."""

_BYTE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]
_BIT_UNITS = ["bps", "Kbps", "Mbps", "Gbps", "Tbps"]


def _scale(value, units, step=1000.0):
    value = float(value or 0)
    for unit in units[:-1]:
        if abs(value) < step:
            return value, unit
        value /= step
    return value, units[-1]


def _num(value):
    if value >= 100:
        return f"{value:.0f}"
    if value >= 10:
        return f"{value:.1f}"
    return f"{value:.2f}" if value else "0"


def speed_parts(bytes_per_sec, unit_mode="bytes"):
    """Return (number, unit) for a transfer rate given in bytes/second."""
    if unit_mode == "bits":
        value, unit = _scale(bytes_per_sec * 8, _BIT_UNITS)
        return _num(value), unit
    value, unit = _scale(bytes_per_sec, _BYTE_UNITS)
    return _num(value), unit + "/s"


def speed(bytes_per_sec, unit_mode="bytes"):
    number, unit = speed_parts(bytes_per_sec, unit_mode)
    return f"{number} {unit}"


FIGURE_SPACE = " "  # as wide as a digit, keeps panel text from jumping


def speed_fixed(bytes_per_sec, unit_mode="bytes"):
    """Constant width rate for panel labels, e.g. '  1.2 MB/s' (never below KB/s)."""
    if unit_mode == "bits":
        value, unit = _scale(max(bytes_per_sec, 0) * 8 / 1000.0, ["Kbps", "Mbps", "Gbps", "Tbps"])
    else:
        value, unit = _scale(max(bytes_per_sec, 0) / 1000.0, ["KB/s", "MB/s", "GB/s", "TB/s"])
    return f"{value:.1f}".rjust(5, FIGURE_SPACE) + " " + unit


def speed_compact(bytes_per_sec, unit_mode="bytes"):
    """Very short rate for drawing inside an icon, e.g. '1.2M', '340K'."""
    if unit_mode == "bits":
        value, unit = _scale(max(bytes_per_sec, 0) * 8 / 1000.0, ["k", "m", "g", "t"])
    else:
        value, unit = _scale(max(bytes_per_sec, 0) / 1000.0, ["K", "M", "G", "T"])
    return (f"{value:.1f}" if value < 10 else f"{value:.0f}") + unit


def size(num_bytes, binary=True):
    value, unit = _scale(num_bytes, _BYTE_UNITS, 1024.0 if binary else 1000.0)
    return f"{_num(value)} {unit}"


def data(num_bytes):
    """Network data volume in decimal units (as ISPs and data plans count it)."""
    return size(num_bytes, binary=False)


def percent(value):
    return f"{value:.0f}%" if value >= 10 else f"{value:.1f}%"


def temperature(celsius, unit="C"):
    if celsius is None:
        return "N/A"
    if unit == "F":
        return f"{celsius * 1.8 + 32:.0f} °F"
    return f"{celsius:.0f} °C"


def frequency(mhz):
    if not mhz:
        return "N/A"
    return f"{mhz / 1000:.2f} GHz" if mhz >= 1000 else f"{mhz:.0f} MHz"


def duration(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, _ = divmod(seconds, 60)
    if days:
        return f"{days}d {hours}h {minutes}m"
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def duration_precise(seconds):
    """'45 s', '2 min 13 s', '1 h 05 min' - for short events like outages."""
    seconds = max(0, int(round(seconds)))
    if seconds < 60:
        return f"{seconds} s"
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes} min {seconds} s" if seconds else f"{minutes} min"
    hours, minutes = divmod(minutes, 60)
    if hours < 24:
        return f"{hours} h {minutes:02d} min"
    days, hours = divmod(hours, 24)
    return f"{days} d {hours} h"
