"""Application bootstrap."""

import signal
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtNetwork import QLocalServer, QLocalSocket
from PyQt5.QtWidgets import QApplication

from . import APP_ID, APP_NAME, ORG_NAME, VERSION

SERVER_NAME = f"{APP_ID}-single-instance"


def _activate_running_instance():
    """Ask an already running SpeedX to show itself. Returns True if one answered."""
    sock = QLocalSocket()
    sock.connectToServer(SERVER_NAME)
    if sock.waitForConnected(300):
        sock.write(b"show")
        sock.waitForBytesWritten(300)
        sock.disconnectFromServer()
        return True
    return False


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setApplicationName(APP_ID)
    app.setApplicationDisplayName(APP_NAME)
    app.setOrganizationName(ORG_NAME)
    app.setApplicationVersion(VERSION)
    app.setDesktopFileName(APP_ID)
    app.setQuitOnLastWindowClosed(False)

    if _activate_running_instance():
        return 0
    server = QLocalServer()
    QLocalServer.removeServer(SERVER_NAME)
    server.listen(SERVER_NAME)

    # imported after QApplication exists (theme detection needs it)
    from .config import Config
    from .main_window import MainWindow
    from .theme import theme

    config = Config()
    theme.detect_system()
    theme.apply(config.get("theme"))

    start_hidden = "--minimized" in sys.argv or config.get("start_minimized")
    window = MainWindow(config, start_hidden=start_hidden)

    def on_connection():
        conn = server.nextPendingConnection()
        if conn:
            conn.readyRead.connect(window.show_and_raise)

    server.newConnection.connect(on_connection)
    signal.signal(signal.SIGINT, lambda *_: window.quit())
    signal.signal(signal.SIGTERM, lambda *_: window.quit())
    # let Python handle signals while Qt's loop is running
    keepalive = QTimer()
    keepalive.timeout.connect(lambda: None)
    keepalive.start(500)

    return app.exec_()
