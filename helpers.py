#!/usr/bin/env python3

# === IMPORTS ===

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')

from gi.repository import Gtk, Gdk, GtkLayerShell
 
# === HELPERS FOR GTK ===

def makeLayer(window):
    GtkLayerShell.init_for_window(window)

def addClass(widget, cssClass):
    context = widget.get_style_context()
    context.add_class(cssClass)

def toggleWindow(window):
    if window.props.visible:
        window.hide()
    else:
        window.show_all()

def setStylesheet(file):
    cssProvider = Gtk.CssProvider()
    cssProvider.load_from_path(file)
    screen = Gdk.Screen.get_default()
    styleContext = Gtk.StyleContext()
    styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER) # With the others GTK_STYLE_PROVIDER_PRIORITY values get the same result.

def createWindow(title, contents):
    window = Gtk.Window()
    window.set_title(title)
    window.add(contents)
    return window

def layeredWindow(title, contents, anchors="", margins="tlbr", layer=GtkLayerShell.Layer.TOP, exclusive=False, monitor=None):
    window = createWindow(title, contents)
    makeLayer(window)

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
