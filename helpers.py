# === IMPORTS ===

import gi
import json
import os
import subprocess

gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')

from gi.repository import Gtk, Gdk, GtkLayerShell

# === HELPERS FOR SYSTEM STUFF ===

def getBattery():
    """Attempt to get battery info by looking at /sys/class/power_supply/BAT0/capacity"""
    try:
        return {
            "charge": int(os.popen("cat /sys/class/power_supply/BAT0/capacity").read().strip())/100,
            "status": os.popen("cat /sys/class/power_supply/BAT0/status").read()
        }
    except:
        return {
            "error": "failed to access battery"
        }

# === HELPERS FOR HYPRCTRL ===

def getMonitors():
    """Attempts to get a list containing maps of monitor information from hyprctl."""
    try:
        return json.loads(subprocess.check_output(["hyprctl", "monitors", "-j"]))
    except:
        return [
            {
                "name": "⚠",
                "id": "1",
                "activeWorkspace": {
                    "id": "1"
                }
            }
        ]

def getWorkspaces():
    """Attempts to get a list containing maps of workspace information from hyprctl."""
    try:
        return json.loads(subprocess.check_output(["hyprctl", "workspaces", "-j"]))
    except:
        return []

# === HELPERS FOR GTK ===

def newWindow(title, contents):
    """Creates a gtk window."""
    window = Gtk.Window()
    window.set_title(title)
    window.add(contents)
    return window

def addClass(widget, cssClass):
    """Adds a class to a widget."""
    widget.get_style_context().add_class(cssClass)


def toggleWindow(window):
    """Toggles the visibility for a window"""
    if window.props.visible:
        window.hide()
    else:
        window.show_all()

def newBox(orientation, spacing, classes, startWidgets, centerWidget, endWidgets):
    """Creates a gtk box widget."""
    box = Gtk.Box(orientation=orientation, spacing=spacing)
    for boxClass in classes:
        addClass(box, boxClass)
    for startWidget in startWidgets:
        box.pack_start(startWidget, False, False, 0)
    for endWidget in endWidgets:
        box.pack_end(endWidget, False, False, 0)
    box.set_center_widget(centerWidget)
    return box

def setStylesheet(file):
    """Sets the stylesheet for your gtk application."""
    cssProvider = Gtk.CssProvider()
    cssProvider.load_from_path(file)
    screen = Gdk.Screen.get_default()
    styleContext = Gtk.StyleContext()
    # With the others GTK_STYLE_PROVIDER_PRIORITY values get the same result.
    styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

# === HELPERS FOR GTK LAYER SHELL ===

def windowToLayer(window):
    """Initialises GtkLayerShell for a window."""
    GtkLayerShell.init_for_window(window)

def layeredWindow(title, contents, anchors="", margins="tlbr", layer=GtkLayerShell.Layer.TOP, exclusive=False, monitor=None):
    """Creates a window that is a GtkLayerShell layer."""
    window = newWindow(title, contents)
    windowToLayer(window)

    # set anchors
    GtkLayerShell.set_anchor(window, GtkLayerShell.Edge.BOTTOM, 1 if anchors.__contains__("b") else 0)
    GtkLayerShell.set_anchor(window, GtkLayerShell.Edge.TOP,    1 if anchors.__contains__("t") else 0)
    GtkLayerShell.set_anchor(window, GtkLayerShell.Edge.LEFT,   1 if anchors.__contains__("l") else 0)
    GtkLayerShell.set_anchor(window, GtkLayerShell.Edge.RIGHT,  1 if anchors.__contains__("r") else 0)

    # set margins
    GtkLayerShell.set_margin(window, GtkLayerShell.Edge.BOTTOM, 10 if margins.__contains__("b") else 0)
    GtkLayerShell.set_margin(window, GtkLayerShell.Edge.TOP,    10 if margins.__contains__("t") else 0)
    GtkLayerShell.set_margin(window, GtkLayerShell.Edge.LEFT,   10 if margins.__contains__("l") else 0)
    GtkLayerShell.set_margin(window, GtkLayerShell.Edge.RIGHT,  10 if margins.__contains__("r") else 0)

    # set exclusive zone
    if exclusive:
        GtkLayerShell.auto_exclusive_zone_enable(window)

    # set layer
    GtkLayerShell.set_layer(window, layer)

    # set monitor
    if monitor != None:
        GtkLayerShell.set_monitor(window, monitor)

    return window

