"""Minimal StatusNotifierItem + com.canonical.dbusmenu implementation.

Qt's QSystemTrayIcon cannot show a text label next to the tray icon. The
Ayatana/AppIndicator extension used by Ubuntu GNOME (and the indicator applets
of XFCE, MATE and Budgie) render the `XAyatanaLabel` property as text in the
panel, which is how SpeedX shows live speed in the top bar. This module talks
D-Bus directly through the pure Python `jeepney` library.

A background thread receives method calls; replies and signals may be sent
from any thread (jeepney's threading connection serialises sends).
"""

import itertools
import os
import sys
import threading
from array import array

from jeepney import DBusAddress, HeaderFields, MessageType, new_error, new_method_call, new_method_return, new_signal
from jeepney.bus_messages import MatchRule, message_bus
from jeepney.io.threading import ReceiveStopped, open_dbus_connection

WATCHER = DBusAddress("/StatusNotifierWatcher", bus_name="org.kde.StatusNotifierWatcher",
                      interface="org.kde.StatusNotifierWatcher")
ITEM_PATH = "/StatusNotifierItem"
ITEM_IFACE = "org.kde.StatusNotifierItem"
MENU_PATH = "/MenuBar"
MENU_IFACE = "com.canonical.dbusmenu"
PROPS_IFACE = "org.freedesktop.DBus.Properties"
INTROSPECT_IFACE = "org.freedesktop.DBus.Introspectable"

_ITEM_XML = """<node><interface name="org.kde.StatusNotifierItem">
<property name="Category" type="s" access="read"/><property name="Id" type="s" access="read"/>
<property name="Title" type="s" access="read"/><property name="Status" type="s" access="read"/>
<property name="IconName" type="s" access="read"/><property name="IconPixmap" type="a(iiay)" access="read"/>
<property name="IconThemePath" type="s" access="read"/>
<property name="OverlayIconName" type="s" access="read"/><property name="OverlayIconPixmap" type="a(iiay)" access="read"/>
<property name="AttentionIconName" type="s" access="read"/>
<property name="AttentionIconPixmap" type="a(iiay)" access="read"/>
<property name="AttentionMovieName" type="s" access="read"/>
<property name="ToolTip" type="(sa(iiay)ss)" access="read"/><property name="ItemIsMenu" type="b" access="read"/>
<property name="Menu" type="o" access="read"/><property name="XAyatanaLabel" type="s" access="read"/>
<property name="XAyatanaLabelGuide" type="s" access="read"/>
<property name="XAyatanaOrderingIndex" type="u" access="read"/>
<method name="Activate"><arg name="x" type="i" direction="in"/><arg name="y" type="i" direction="in"/></method>
<method name="SecondaryActivate"><arg name="x" type="i" direction="in"/><arg name="y" type="i" direction="in"/></method>
<method name="XAyatanaSecondaryActivate"><arg name="timestamp" type="u" direction="in"/></method>
<method name="ContextMenu"><arg name="x" type="i" direction="in"/><arg name="y" type="i" direction="in"/></method>
<method name="Scroll"><arg name="delta" type="i" direction="in"/><arg name="orientation" type="s" direction="in"/></method>
<signal name="NewTitle"/><signal name="NewIcon"/><signal name="NewAttentionIcon"/><signal name="NewOverlayIcon"/>
<signal name="NewToolTip"/><signal name="NewStatus"><arg name="status" type="s"/></signal>
<signal name="XAyatanaNewLabel"><arg name="label" type="s"/><arg name="guide" type="s"/></signal>
</interface></node>"""

_MENU_XML = """<node><interface name="com.canonical.dbusmenu">
<property name="Version" type="u" access="read"/><property name="TextDirection" type="s" access="read"/>
<property name="Status" type="s" access="read"/><property name="IconThemePath" type="as" access="read"/>
<method name="GetLayout"><arg type="i" direction="in"/><arg type="i" direction="in"/><arg type="as" direction="in"/>
<arg type="u" direction="out"/><arg type="(ia{sv}av)" direction="out"/></method>
<method name="GetGroupProperties"><arg type="ai" direction="in"/><arg type="as" direction="in"/>
<arg type="a(ia{sv})" direction="out"/></method>
<method name="GetProperty"><arg type="i" direction="in"/><arg type="s" direction="in"/>
<arg type="v" direction="out"/></method>
<method name="Event"><arg type="i" direction="in"/><arg type="s" direction="in"/><arg type="v" direction="in"/>
<arg type="u" direction="in"/></method>
<method name="EventGroup"><arg type="a(isvu)" direction="in"/><arg type="ai" direction="out"/></method>
<method name="AboutToShow"><arg type="i" direction="in"/><arg type="b" direction="out"/></method>
<method name="AboutToShowGroup"><arg type="ai" direction="in"/><arg type="ai" direction="out"/>
<arg type="ai" direction="out"/></method>
<signal name="ItemsPropertiesUpdated"><arg type="a(ia{sv})"/><arg type="a(ias)"/></signal>
<signal name="LayoutUpdated"><arg type="u"/><arg type="i"/></signal>
</interface></node>"""


def image_to_pixmap(image):
    """QImage -> (width, height, ARGB32 bytes in network byte order) as the SNI spec wants."""
    from PyQt5.QtGui import QImage
    img = image.convertToFormat(QImage.Format_ARGB32)
    ptr = img.constBits()
    ptr.setsize(img.byteCount())
    data = array("I")
    data.frombytes(bytes(ptr))
    if sys.byteorder == "little":
        data.byteswap()
    return (img.width(), img.height(), data.tobytes())


class MenuItem:
    def __init__(self, label="", callback=None, separator=False, checkable=False, checked=False, enabled=True):
        self.label = label
        self.callback = callback
        self.separator = separator
        self.checkable = checkable
        self.checked = checked
        self.enabled = enabled

    def props(self):
        if self.separator:
            return {"type": ("s", "separator")}
        props = {"label": ("s", self.label), "enabled": ("b", self.enabled), "visible": ("b", True)}
        if self.checkable:
            props["toggle-type"] = ("s", "checkmark")
            props["toggle-state"] = ("i", 1 if self.checked else 0)
        return props


class StatusNotifierItem:
    """Publishes one tray item. Callbacks run on the D-Bus thread: keep them thread safe
    (emitting a Qt signal is)."""

    def __init__(self, item_id, title, on_activate=None):
        self.item_id = item_id
        self.title = title
        self.on_activate = on_activate
        self.status = "Active"
        self.label = ""
        self.label_guide = ""
        self.icon_pixmaps = []
        self.tooltip = ("", [], title, "")
        self.menu_items = []        # list[MenuItem]; ids are index + 1
        self._revision = 1
        self._conn = None
        self._thread = None
        self._serial = itertools.count(1000)
        self.bus_name = f"org.kde.StatusNotifierItem-{os.getpid()}-1"

    # ---------------------------------------------------------------- setup
    @staticmethod
    def watcher_available():
        """True when a StatusNotifierWatcher (tray host) runs on the session bus."""
        try:
            conn = open_dbus_connection("SESSION")
        except (OSError, ValueError, KeyError):
            return False
        try:
            msg = new_method_call(message_bus, "NameHasOwner", "s", (WATCHER.bus_name,))
            reply = StatusNotifierItem._call_sync(conn, msg)
            return bool(reply and reply.body[0])
        except Exception:  # noqa: BLE001 - any failure means "not available"
            return False
        finally:
            conn.close()

    @staticmethod
    def _call_sync(conn, msg, timeout=1.0):
        serial = next(StatusNotifierItem._sync_serial)
        conn.send(msg, serial=serial)
        while True:
            reply = conn.receive(timeout=timeout)
            if reply.header.fields.get(HeaderFields.reply_serial) == serial:
                return reply if reply.header.message_type == MessageType.method_return else None

    _sync_serial = itertools.count(1)

    def start(self):
        self._conn = open_dbus_connection("SESSION")
        self._send(new_method_call(message_bus, "RequestName", "su", (self.bus_name, 4)))
        rule = MatchRule(type="signal", sender=message_bus.bus_name, interface=message_bus.interface,
                         member="NameOwnerChanged", path=message_bus.object_path)
        rule.add_arg_condition(0, WATCHER.bus_name)
        self._send(new_method_call(message_bus, "AddMatch", "s", (rule.serialise(),)))
        self._register()
        self._thread = threading.Thread(target=self._loop, name="sni", daemon=True)
        self._thread.start()

    def stop(self):
        if self._conn is None:
            return
        try:
            self._send(new_method_call(message_bus, "ReleaseName", "s", (self.bus_name,)))
        except OSError:
            pass
        self._conn.close()
        self._conn = None

    def _register(self):
        self._send(new_method_call(WATCHER, "RegisterStatusNotifierItem", "s", (self.bus_name,)))

    def _send(self, msg):
        if self._conn is not None:
            self._conn.send(msg, serial=next(self._serial))

    # --------------------------------------------------------------- public
    def set_label(self, label, guide=""):
        if label == self.label and guide == self.label_guide:
            return
        self.label, self.label_guide = label, guide
        self._emit(ITEM_PATH, ITEM_IFACE, "XAyatanaNewLabel", "ss", (label, guide))

    def set_icon(self, pixmaps):
        self.icon_pixmaps = pixmaps
        self._emit(ITEM_PATH, ITEM_IFACE, "NewIcon")

    def set_tooltip(self, title, body):
        self.tooltip = ("", [], title, body)
        self._emit(ITEM_PATH, ITEM_IFACE, "NewToolTip")

    def set_status(self, status):
        """'Active' or 'Passive' (hidden by most hosts)."""
        if status != self.status:
            self.status = status
            self._emit(ITEM_PATH, ITEM_IFACE, "NewStatus", "s", (status,))

    def set_menu(self, items):
        self.menu_items = items
        self.menu_changed()

    def menu_changed(self):
        self._revision += 1
        self._emit(MENU_PATH, MENU_IFACE, "LayoutUpdated", "ui", (self._revision, 0))

    def _emit(self, path, iface, name, signature=None, body=()):
        if self._conn is None:
            return
        try:
            self._send(new_signal(DBusAddress(path, interface=iface), name, signature, body))
        except OSError:
            pass

    # ------------------------------------------------------------ receiving
    def _loop(self):
        while True:
            conn = self._conn
            if conn is None:
                return
            try:
                msg = conn.receive()
            except (ReceiveStopped, OSError, ValueError):
                return
            try:
                self._dispatch(msg)
            except Exception as exc:  # noqa: BLE001 - never kill the D-Bus thread
                if msg.header.message_type == MessageType.method_call:
                    self._send(new_error(msg, "org.freedesktop.DBus.Error.Failed", "s", (str(exc),)))

    def _dispatch(self, msg):
        fields = msg.header.fields
        if msg.header.message_type == MessageType.signal:
            if fields.get(HeaderFields.member) == "NameOwnerChanged" and msg.body[0] == WATCHER.bus_name and msg.body[2]:
                self._register()  # tray host restarted (e.g. GNOME Shell reload)
            return
        if msg.header.message_type != MessageType.method_call:
            return
        path = fields.get(HeaderFields.path)
        iface = fields.get(HeaderFields.interface)
        member = fields.get(HeaderFields.member)

        if iface == INTROSPECT_IFACE:
            xml = {ITEM_PATH: _ITEM_XML, MENU_PATH: _MENU_XML}.get(path, "<node/>")
            return self._send(new_method_return(msg, "s", (xml,)))
        if iface == PROPS_IFACE:
            return self._properties(msg, path, member)
        if path == ITEM_PATH:
            return self._item_call(msg, member)
        if path == MENU_PATH:
            return self._menu_call(msg, member)
        self._send(new_error(msg, "org.freedesktop.DBus.Error.UnknownObject"))

    def _item_props(self):
        empty = []
        return {
            "Category": ("s", "Hardware"),
            "Id": ("s", self.item_id),
            "Title": ("s", self.title),
            "Status": ("s", self.status),
            "IconName": ("s", ""),
            "IconThemePath": ("s", ""),
            "IconPixmap": ("a(iiay)", self.icon_pixmaps),
            "OverlayIconName": ("s", ""),
            "OverlayIconPixmap": ("a(iiay)", empty),
            "AttentionIconName": ("s", ""),
            "AttentionIconPixmap": ("a(iiay)", empty),
            "AttentionMovieName": ("s", ""),
            "ToolTip": ("(sa(iiay)ss)", self.tooltip),
            "ItemIsMenu": ("b", False),
            "Menu": ("o", MENU_PATH),
            "XAyatanaLabel": ("s", self.label),
            "XAyatanaLabelGuide": ("s", self.label_guide),
            "XAyatanaOrderingIndex": ("u", 0),
        }

    @staticmethod
    def _menu_props():
        return {
            "Version": ("u", 3),
            "TextDirection": ("s", "ltr"),
            "Status": ("s", "normal"),
            "IconThemePath": ("as", []),
        }

    def _properties(self, msg, path, member):
        props = self._item_props() if path == ITEM_PATH else self._menu_props()
        if member == "GetAll":
            return self._send(new_method_return(msg, "a{sv}", (props,)))
        if member == "Get":
            name = msg.body[1]
            if name in props:
                return self._send(new_method_return(msg, "v", (props[name],)))
            return self._send(new_error(msg, "org.freedesktop.DBus.Error.InvalidArgs", "s", (f"No property {name}",)))
        self._send(new_error(msg, "org.freedesktop.DBus.Error.PropertyReadOnly"))

    def _item_call(self, msg, member):
        if member == "Activate" and self.on_activate:
            self.on_activate()
        self._send(new_method_return(msg))

    def _menu_entry(self, item_id):
        props = {"children-display": ("s", "submenu")} if item_id == 0 else self.menu_items[item_id - 1].props()
        children = []
        if item_id == 0:
            children = [("(ia{sv}av)", (i + 1, item.props(), [])) for i, item in enumerate(self.menu_items)]
        return (item_id, props, children)

    def _menu_call(self, msg, member):
        if member == "GetLayout":
            parent = msg.body[0]
            parent = parent if 0 <= parent <= len(self.menu_items) else 0
            return self._send(new_method_return(msg, "u(ia{sv}av)", (self._revision, self._menu_entry(parent))))
        if member == "GetGroupProperties":
            ids = msg.body[0] or range(len(self.menu_items) + 1)
            result = [(i, self._menu_entry(i)[1]) for i in ids if 0 <= i <= len(self.menu_items)]
            return self._send(new_method_return(msg, "a(ia{sv})", (result,)))
        if member == "GetProperty":
            item_id, name = msg.body
            props = self._menu_entry(item_id)[1] if 0 <= item_id <= len(self.menu_items) else {}
            return self._send(new_method_return(msg, "v", (props.get(name, ("s", "")),)))
        if member == "Event":
            item_id, event_id = msg.body[0], msg.body[1]
            self._send(new_method_return(msg))
            if event_id == "clicked" and 1 <= item_id <= len(self.menu_items):
                item = self.menu_items[item_id - 1]
                if item.callback and item.enabled:
                    item.callback()
            return None
        if member == "EventGroup":
            for item_id, event_id, _data, _ts in msg.body[0]:
                if event_id == "clicked" and 1 <= item_id <= len(self.menu_items):
                    item = self.menu_items[item_id - 1]
                    if item.callback and item.enabled:
                        item.callback()
            return self._send(new_method_return(msg, "ai", ([],)))
        if member == "AboutToShow":
            return self._send(new_method_return(msg, "b", (False,)))
        if member == "AboutToShowGroup":
            return self._send(new_method_return(msg, "aiai", ([], [])))
        self._send(new_error(msg, "org.freedesktop.DBus.Error.UnknownMethod"))
