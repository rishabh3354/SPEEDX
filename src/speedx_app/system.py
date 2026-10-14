"""Static system information and low level sensor helpers."""

import os
import platform
import socket

import psutil

# Preferred temperature sensors, most accurate first. (chip, label prefix or None)
_TEMP_SENSORS = [
    ("coretemp", "Package id"),
    ("k10temp", "Tctl"),
    ("k10temp", "Tdie"),
    ("zenpower", "Tdie"),
    ("cpu_thermal", None),
    ("cpu-thermal", None),
    ("soc_thermal", None),
    ("coretemp", None),
    ("k10temp", None),
    ("acpitz", None),
]

_IGNORED_FS = {"squashfs", "tmpfs", "devtmpfs", "overlay", "proc", "sysfs", "efivarfs", "ramfs"}


def cpu_model():
    try:
        with open("/proc/cpuinfo") as fh:
            for line in fh:
                if line.lower().startswith(("model name", "hardware", "processor\t: arm")):
                    name = line.split(":", 1)[1].strip()
                    if name and not name.isdigit():
                        return " ".join(name.split())
    except OSError:
        pass
    return platform.processor() or platform.machine() or "Unknown CPU"


def os_name():
    try:
        with open("/etc/os-release") as fh:
            for line in fh:
                if line.startswith("PRETTY_NAME="):
                    return line.split("=", 1)[1].strip().strip('"')
    except OSError:
        pass
    return f"{platform.system()} {platform.release()}"


def static_info():
    return {
        "hostname": platform.node(),
        "os": os_name(),
        "kernel": platform.release(),
        "arch": platform.machine(),
        "cpu_model": cpu_model(),
        "cores": psutil.cpu_count(logical=False) or psutil.cpu_count() or 1,
        "threads": psutil.cpu_count() or 1,
        "boot_time": psutil.boot_time(),
    }


def cpu_temperature():
    """Return the CPU temperature in °C, or None when no sensor is readable."""
    try:
        sensors = psutil.sensors_temperatures()
    except (AttributeError, OSError):
        return None
    if not sensors:
        return None
    for chip, label in _TEMP_SENSORS:
        entries = sensors.get(chip)
        if not entries:
            continue
        for entry in entries:
            if entry.current and (label is None or (entry.label or "").startswith(label)):
                return float(entry.current)
    return None


def cpu_frequency():
    try:
        freq = psutil.cpu_freq()
        return freq.current if freq else None
    except (AttributeError, OSError, NotImplementedError):
        return None


def load_average():
    try:
        return os.getloadavg()
    except OSError:
        return (0.0, 0.0, 0.0)


_VIRTUAL_PREFIXES = ("lo", "docker", "veth", "br-", "virbr", "lxdbr", "lxcbr", "vmnet", "vboxnet",
                     "tun", "tap", "wg", "zt", "tailscale", "cni", "flannel", "podman", "kube")


def is_physical(name):
    """True for real network adapters (Wi-Fi, Ethernet, USB tethering, modems).

    Virtual links (containers, bridges, VPN tunnels) are excluded from totals:
    their traffic also crosses a physical adapter, so it would be counted twice.
    """
    if os.path.isdir("/sys/class/net"):
        return os.path.exists(f"/sys/class/net/{name}/device")
    return not name.startswith(_VIRTUAL_PREFIXES)


def network_interfaces():
    """Names of non loopback network interfaces."""
    try:
        stats = psutil.net_if_stats()
    except OSError:
        return []
    return sorted(name for name in stats if name != "lo" and not name.startswith("lo:"))


def local_ip():
    """Address of the interface used for the default route (no packets are sent)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("1.1.1.1", 80))
            return sock.getsockname()[0]
    except OSError:
        return None


def interface_details():
    """List of dicts describing each network interface."""
    try:
        stats = psutil.net_if_stats()
        addrs = psutil.net_if_addrs()
    except OSError:
        return []
    result = []
    for name in network_interfaces():
        st = stats.get(name)
        ipv4 = next((a.address for a in addrs.get(name, []) if a.family == socket.AF_INET), "")
        mac = next((a.address for a in addrs.get(name, []) if a.family == psutil.AF_LINK), "")
        result.append({
            "name": name,
            "up": bool(st and st.isup),
            "speed": st.speed if st else 0,
            "ipv4": ipv4,
            "mac": mac,
        })
    return result


def disk_partitions():
    result = []
    seen = set()
    try:
        parts = psutil.disk_partitions(all=False)
    except OSError:
        return result
    for part in parts:
        if part.fstype in _IGNORED_FS or part.device in seen:
            continue
        if part.mountpoint.startswith(("/snap", "/var/snap", "/boot/efi")) or "/loop" in part.device:
            continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except (PermissionError, OSError):
            continue
        if usage.total <= 0:
            continue
        seen.add(part.device)
        result.append({
            "device": part.device,
            "mount": part.mountpoint,
            "fstype": part.fstype,
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": usage.percent,
        })
    return result
