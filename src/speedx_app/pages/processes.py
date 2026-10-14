import os
from collections import defaultdict

import psutil
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAbstractItemView, QHeaderView, QLineEdit, QMenu, QMessageBox, QPushButton,
                             QTreeWidget, QTreeWidgetItem)

from .. import formatting as fmt
from ..apps import KERNEL
from ..theme import theme
from ..widgets.common import Card, Page, Toggle, label

COLUMNS = ["Name", "PID", "User", "CPU", "Memory", "Status"]
RIGHT = (1, 3, 4)
SORT_ROLE = Qt.UserRole + 1
KEY_ROLE = Qt.UserRole + 2
PROTECTED = {0, 1, os.getpid()}


class _Item(QTreeWidgetItem):
    def __lt__(self, other):
        col = self.treeWidget().sortColumn() if self.treeWidget() else 0
        a, b = self.data(col, SORT_ROLE), other.data(col, SORT_ROLE)
        if a is None or b is None:
            return super().__lt__(other)
        return a < b


class ProcessesPage(Page):
    needs_processes = True

    def __init__(self, ctx):
        super().__init__("Processes", "Running applications and background tasks")
        self.ctx = ctx
        self._expanded = set()
        self._selected = None          # ("group", name) or ("proc", pid)
        self._rows = []

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search by name, app, user or PID")
        self.search.setClearButtonEnabled(True)
        self.search.setMinimumWidth(260)
        self.search.textChanged.connect(lambda _: self._rebuild())
        self.group_toggle = Toggle(ctx.config.get("group_processes"))
        self.group_toggle.toggled.connect(self._group_changed)
        self.end_btn = QPushButton("End process")
        self.end_btn.setObjectName("Danger")
        self.end_btn.setEnabled(False)
        self.end_btn.clicked.connect(lambda: self._end(force=False))
        self.actions.addWidget(self.search)
        self.actions.addSpacing(6)
        self.actions.addWidget(label("Group by app", "Muted"))
        self.actions.addWidget(self.group_toggle)
        self.actions.addSpacing(6)
        self.actions.addWidget(self.end_btn)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(len(COLUMNS))
        self.tree.setHeaderLabels(COLUMNS)
        self.tree.setUniformRowHeights(True)
        self.tree.setRootIsDecorated(True)
        self.tree.setAlternatingRowColors(False)
        self.tree.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tree.setSortingEnabled(True)
        self.tree.sortByColumn(3, Qt.DescendingOrder)
        header = self.tree.header()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setStretchLastSection(False)
        for col, width in ((1, 90), (2, 120), (3, 90), (4, 100), (5, 100)):
            header.setSectionResizeMode(col, QHeaderView.Interactive)
            self.tree.setColumnWidth(col, width)
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        for col in RIGHT:
            self.tree.headerItem().setTextAlignment(col, Qt.AlignRight | Qt.AlignVCenter)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._context_menu)
        self.tree.itemSelectionChanged.connect(self._selection_changed)
        self.tree.itemExpanded.connect(lambda it: self._expanded.add(it.data(0, KEY_ROLE)[1]))
        self.tree.itemCollapsed.connect(lambda it: self._expanded.discard(it.data(0, KEY_ROLE)[1]))
        self.tree.setMinimumHeight(480)

        self.count = label("", "Faint")
        card = Card(padding=8, spacing=6)
        card.add(self.tree, 1)
        self.add(card, 1)
        self.add(self.count)

    # ------------------------------------------------------------- helpers
    def _group_changed(self, grouped):
        self.ctx.config.set("group_processes", bool(grouped))
        self._rebuild()

    def _cells(self, item, values, sort_values):
        for col, (text, key) in enumerate(zip(values, sort_values)):
            item.setText(col, text)
            item.setData(col, SORT_ROLE, key)
            if col in RIGHT:
                item.setTextAlignment(col, Qt.AlignRight | Qt.AlignVCenter)

    def _proc_item(self, row, show_app=False):
        pid, name, user, cpu, rss, _pct, status, app = row
        item = _Item()
        title = f"{name}  ·  {app}" if show_app and app and app != name else name
        self._cells(item, [title, str(pid), user, fmt.percent(cpu), fmt.size(rss), status],
                    [name.lower(), pid, user.lower(), cpu, rss, status])
        item.setData(0, KEY_ROLE, ("proc", pid))
        muted = theme.color("muted")
        for col in (1, 2, 5):
            item.setForeground(col, muted)
        if cpu >= 50:
            item.setForeground(3, theme.color("bad" if cpu >= 80 else "warn"))
        return item

    def _group_item(self, app, rows):
        cpu = sum(r[3] for r in rows)
        rss = sum(r[4] for r in rows)
        users = {r[2] for r in rows}
        user = users.pop() if len(users) == 1 else "multiple"
        item = _Item()
        self._cells(item, [f"{app}  ({len(rows)})", "", user, fmt.percent(cpu), fmt.size(rss), ""],
                    [app.lower(), len(rows), user.lower(), cpu, rss, ""])
        item.setData(0, KEY_ROLE, ("group", app))
        font = item.font(0)
        font.setBold(True)
        item.setFont(0, font)
        item.setForeground(1, theme.color("muted"))
        if cpu >= 50:
            item.setForeground(3, theme.color("bad" if cpu >= 80 else "warn"))
        return item

    @staticmethod
    def _matches(row, text):
        pid, name, user, *_rest, app = row
        return text in name.lower() or text in user.lower() or text in (app or "").lower() or text == str(pid)

    # ------------------------------------------------------------- refresh
    def _rebuild(self):
        rows = self._rows
        text = self.search.text().strip().lower()
        grouped = self.group_toggle.isChecked()
        scroll = self.tree.verticalScrollBar().value()
        selected = self._selected

        self.tree.setUpdatesEnabled(False)
        self.tree.blockSignals(True)
        sort_col, sort_order = self.tree.sortColumn(), self.tree.header().sortIndicatorOrder()
        self.tree.setSortingEnabled(False)
        self.tree.clear()
        select_item = None
        shown = 0

        if grouped:
            groups = defaultdict(list)
            for row in rows:
                groups[row[7] or row[1]].append(row)
            for app, members in groups.items():
                if text:
                    if text in app.lower():
                        visible = members
                    else:
                        visible = [r for r in members if self._matches(r, text)]
                    if not visible:
                        continue
                else:
                    visible = members
                shown += len(visible)
                if len(members) == 1 and app != KERNEL[1]:
                    item = self._proc_item(members[0], show_app=True)
                    self.tree.addTopLevelItem(item)
                    if selected == ("proc", members[0][0]):
                        select_item = item
                    continue
                group = self._group_item(app, visible)
                self.tree.addTopLevelItem(group)
                for row in visible:
                    child = self._proc_item(row)
                    group.addChild(child)
                    if selected == ("proc", row[0]):
                        select_item = child
                if selected == ("group", app):
                    select_item = group
                if app in self._expanded or (text and app != KERNEL[1]):
                    group.setExpanded(True)
        else:
            for row in rows:
                if text and not self._matches(row, text):
                    continue
                shown += 1
                item = self._proc_item(row, show_app=False)
                self.tree.addTopLevelItem(item)
                if selected == ("proc", row[0]):
                    select_item = item

        self.tree.setSortingEnabled(True)
        self.tree.sortByColumn(sort_col, sort_order)
        if select_item is not None:
            select_item.setSelected(True)
            self.tree.setCurrentItem(select_item)
        self.tree.blockSignals(False)
        self.tree.verticalScrollBar().setValue(scroll)
        self.tree.setUpdatesEnabled(True)
        self._selected = selected if select_item is not None else None
        self._update_button()

        total = len(rows)
        apps = len({r[7] for r in rows if r[7] and r[7] != KERNEL[1]})
        summary = f"{total} processes" + (f" in {apps} apps and services" if grouped else "")
        self.count.setText(summary if shown == total else f"Showing {shown} of {total} processes")

    def on_snapshot(self, snap, monitor):
        if snap["processes"] is None:
            return
        self._rows = monitor.processes
        self._rebuild()

    # ------------------------------------------------------------- actions
    def _selection_changed(self):
        items = self.tree.selectedItems()
        self._selected = items[0].data(0, KEY_ROLE) if items else None
        self._update_button()

    def _update_button(self):
        kind = self._selected[0] if self._selected else None
        self.end_btn.setEnabled(kind is not None and self._selected != ("group", KERNEL[1]))
        self.end_btn.setText("End app" if kind == "group" else "End process")

    def _context_menu(self, pos):
        item = self.tree.itemAt(pos)
        if item is None:
            return
        self.tree.setCurrentItem(item)
        self._selected = item.data(0, KEY_ROLE)
        if self._selected == ("group", KERNEL[1]):
            return
        noun = "app" if self._selected[0] == "group" else "process"
        menu = QMenu(self)
        menu.addAction(f"End {noun}", lambda: self._end(force=False))
        menu.addAction(f"Force kill {noun}", lambda: self._end(force=True))
        menu.exec_(self.tree.viewport().mapToGlobal(pos))

    def _targets(self):
        if not self._selected:
            return None, []
        kind, key = self._selected
        if kind == "group":
            pids = [r[0] for r in self._rows if (r[7] or r[1]) == key]
            return key, [p for p in pids if p not in PROTECTED]
        name = next((r[1] for r in self._rows if r[0] == key), str(key))
        return f"{name} (PID {key})", ([key] if key not in PROTECTED else [])

    def _end(self, force=False):
        title, pids = self._targets()
        if not pids:
            if title:
                QMessageBox.information(self, "Not allowed", "SpeedX won't stop itself or core system processes.")
            return
        verb = "Force kill" if force else "End"
        extra = f"\n\nThis stops {len(pids)} processes." if len(pids) > 1 else ""
        answer = QMessageBox.question(
            self, f"{verb} {title}",
            f"{verb} “{title}”?{extra}\n\nUnsaved work in this application will be lost.",
            QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
        if answer != QMessageBox.Yes:
            return
        denied = 0
        for pid in pids:
            try:
                proc = psutil.Process(pid)
                proc.kill() if force else proc.terminate()
            except psutil.AccessDenied:
                denied += 1
            except psutil.NoSuchProcess:
                pass
        if denied:
            QMessageBox.warning(self, "Permission denied",
                                f"SpeedX could not stop {denied} of {len(pids)} processes. They probably belong "
                                "to another user or the system.")
