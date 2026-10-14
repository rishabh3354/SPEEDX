"""CSV export with a save dialog."""

import csv
import datetime as dt
import os

from PyQt5.QtCore import QStandardPaths, QTimer
from PyQt5.QtWidgets import QFileDialog, QMessageBox


def save_csv(parent, base_name, header, rows, button=None):
    """Ask where to save, write the CSV and briefly confirm on `button`. Returns the path or None."""
    folder = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation) or os.path.expanduser("~")
    default = os.path.join(folder, f"{base_name}-{dt.date.today().isoformat()}.csv")
    path, _ = QFileDialog.getSaveFileName(parent, "Export CSV", default, "CSV files (*.csv)")
    if not path:
        return None
    if not path.lower().endswith(".csv"):
        path += ".csv"
    try:
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(header)
            writer.writerows(rows)
    except OSError as exc:
        QMessageBox.warning(parent, "Export failed", f"Could not save the file:\n{exc}")
        return None
    if button is not None:
        original = button.text()
        button.setText("Saved ✓")
        QTimer.singleShot(2500, lambda: button.setText(original))
    return path
