"""Map processes to the desktop application they belong to.

Modern desktops launch every application in its own systemd scope, e.g.
  app-gnome-google\\x2dchrome-18261.scope
  app-com.anthropic.Claude-19777.scope
  snap.firefox.firefox-1f2e....scope
so /proc/<pid>/cgroup tells which app a helper process belongs to. The app id
is resolved to a friendly name through its .desktop file.
"""

import os
import re

_DESKTOP_DIRS = [
    os.path.expanduser("~/.local/share/applications"),
    os.path.expanduser("~/.local/share/flatpak/exports/share/applications"),
    "/var/lib/flatpak/exports/share/applications",
    "/var/lib/snapd/desktop/applications",
    "/usr/local/share/applications",
    "/usr/share/applications",
    "/var/lib/snapd/hostfs/usr/share/applications",  # host files when running as a snap
]
_LAUNCHER_PREFIXES = ("gnome-launched-", "gnome-", "flatpak-", "kde-", "xfce4-", "xfce-", "dbus-", "cosmic-")
_ESCAPE = re.compile(r"\\x([0-9a-fA-F]{2})")
_INSTANCE = re.compile(r"^[0-9a-fA-F]+$")

KERNEL = ("kernel", "Kernel threads")
TERMINAL = ("terminal", "Terminal sessions")

_name_cache = {}


def _unescape(text):
    return _ESCAPE.sub(lambda m: chr(int(m.group(1), 16)), text)


def _desktop_name(app_id):
    if app_id in _name_cache:
        return _name_cache[app_id]
    name = None
    for directory in _DESKTOP_DIRS:
        path = os.path.join(directory, app_id + ".desktop")
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                in_entry = False
                for line in fh:
                    line = line.strip()
                    if line.startswith("["):
                        in_entry = line == "[Desktop Entry]"
                    elif in_entry and line.startswith("Name="):
                        name = line[5:].strip()
                        break
        except OSError:
            continue
        if name:
            break
    _name_cache[app_id] = name
    return name


def _pretty(app_id):
    base = app_id.split(".")[-1] if "." in app_id and "-" not in app_id.split(".")[-1] else app_id
    base = re.sub(r"[-_](?:[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12})$", "", base)  # trailing UUID
    words = re.split(r"[-_]+", base)
    return " ".join(w[:1].upper() + w[1:] for w in words if w) or app_id


def _app_from_scope(unit):
    """('app id', 'display name') for an app scope / service unit, else None."""
    if unit.startswith("snap."):
        parts = unit.split(".")
        if len(parts) >= 3:
            snap, app = parts[1], parts[2].split("-")[0]
            name = _desktop_name(f"{snap}_{app}") or _desktop_name(f"{snap}_{snap}") or _pretty(snap)
            return name
        return None
    if unit.startswith("vte-spawn-"):
        return TERMINAL[1]
    if not unit.startswith("app-"):
        return None
    body = unit[4:]
    for suffix in (".scope", ".service", ".slice"):
        if body.endswith(suffix):
            body = body[:-len(suffix)]
    if "@" in body:
        body = body.split("@", 1)[0]
    else:
        head, sep, tail = body.rpartition("-")
        if sep and _INSTANCE.match(tail):
            body = head
    body = _unescape(body)
    candidates = [body] + [body[len(p):] for p in _LAUNCHER_PREFIXES if body.startswith(p)]
    for app_id in candidates:
        name = _desktop_name(app_id)
        if name:
            return name
    return _pretty(candidates[-1])


def group_for(pid, name):
    """Display name of the app a process belongs to (falls back to the process name)."""
    try:
        with open(f"/proc/{pid}/cgroup") as fh:
            line = fh.readline().strip()
    except OSError:
        return name
    path = line.split(":", 2)[-1] if line else ""
    if path in ("", "/"):
        return KERNEL[1]
    for unit in reversed(path.split("/")):
        app = _app_from_scope(unit)
        if app:
            return app
    return name
