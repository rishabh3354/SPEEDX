"""Launch-at-login support via an XDG autostart desktop entry.

Inside a snap, $HOME points at $SNAP_USER_DATA, which is where snapd looks for
the autostart file declared with `autostart: speedx.desktop` in snapcraft.yaml.
"""

import os
import sys

FILE_NAME = "speedx.desktop"


def _path():
    base = os.environ.get("XDG_CONFIG_HOME") if not os.environ.get("SNAP") else None
    base = base or os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(base, "autostart", FILE_NAME)


def _exec_line():
    if os.environ.get("SNAP"):
        return "speedx --minimized"
    script = os.path.abspath(sys.argv[0])
    return f'"{sys.executable}" "{script}" --minimized'


def is_enabled():
    return os.path.exists(_path())


def set_enabled(enabled):
    path = _path()
    try:
        if not enabled:
            if os.path.exists(path):
                os.remove(path)
            return True
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(
                "[Desktop Entry]\n"
                "Type=Application\n"
                "Name=SpeedX\n"
                "Comment=System and internet speed monitor\n"
                f"Exec={_exec_line()}\n"
                "Icon=speedx\n"
                "Terminal=false\n"
                "X-GNOME-Autostart-enabled=true\n"
            )
        return True
    except OSError:
        return False
