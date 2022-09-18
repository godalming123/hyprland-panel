#!/usr/bin/env python3

# === IMPORTS ===

import gi
import helpers
import time
import subprocess
import json

gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')

from gi.repository import Gtk, GtkLayerShell, GLib, Gdk

# === WIDGETS ===

def timeBtn(onclick):
    btn = Gtk.Button()
    
    def updateTime():
        theTime = time.localtime(time.time())
        btn.set_label(str(theTime.tm_hour).zfill(2) + "\n" + str(theTime.tm_min).zfill(2))
        return True
    
    updateTime()
    GLib.timeout_add(15*1000, updateTime)

    btn.connect("clicked", onclick)
    return btn

def hoverRevealer(icon, progress, onChange):
    # === TODO ===
    revealer = Gtk.Revealer()
    revealer.set_reveal_child(Gtk.Label(label="hi"))

def resoarcesWidget(onclick):
    text = Gtk.Label()
    Gtk.Label.set_justify(text, Gtk.Justification.CENTER)

    labelText = ""

    # battery
    labelText += "🔋"
    #labelText += subprocess.check_output("cat /sys/class/power_supply/BAT0/capacity", shell=True)
    labelText += "\n"

    # cpu usage
    labelText += "C"
    labelText += "\n"

    # memory usage
    labelText += "M"

    text.set_label(labelText)
    return text

def workspacesWidget(monitorId):
    text = Gtk.Label()
    Gtk.Label.set_justify(text, Gtk.Justification.CENTER)
    def updateWorkspaces():
        monitors = json.loads(subprocess.check_output(["hyprctl", "monitors", "-j"]))
        workspaces = json.loads(subprocess.check_output(["hyprctl", "workspaces", "-j"]))
        workspacesText = ""
        for monitor in monitors: # loop through monitors
            if monitor["id"] == monitorId: # if monitor is the one we want
                for workspace in workspaces: # then loop through workspaces
                    if workspace["monitor"] == monitor["name"]: # and if the workspace is on the monitor
                        # add it to the text
                        isActive = (monitor["activeWorkspace"]["id"] == workspace["id"])
                        if isActive:
                            workspacesText += "❱"
                        workspacesText += workspace["name"]
                        if isActive:
                            workspacesText += "❰"
                        workspacesText += "\n"

        text.set_label(workspacesText)

        return True
    
    updateWorkspaces()
    GLib.timeout_add(250, updateWorkspaces)

    return text

# === WINDOWS ===

launcher   = helpers.layeredWindow("launcher", Gtk.Label(label="Launcher!")) # TODO
background = helpers.layeredWindow("background", Gtk.Label(label="Background!"), "tlbr", "", GtkLayerShell.Layer.BACKGROUND) # TODO
datemenu   = helpers.layeredWindow("datemenu", Gtk.Calendar(), "bl", "bl")

def makeBar(monitor, monitorId):
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
    helpers.addClass(box, "bar-box")
    searchBtn = Gtk.Button(label="⌥")
    searchBtn.connect("clicked", lambda _: helpers.toggleWindow(launcher))
    helpers.addClass(searchBtn, "search")
    box.set_center_widget(workspacesWidget(monitorId))
    box.pack_start(searchBtn, False, True, 0)
    box.pack_end(timeBtn(lambda _: helpers.toggleWindow(datemenu)), False, True, 0)
    #box.pack_end(resoarcesWidget(None), False, True, 0)
    return helpers.layeredWindow("bar", box, "tlb", "tlb", GtkLayerShell.Layer.TOP, True, monitor)

bars = []

def newBar(monitor, monitorId):
    bar = makeBar(monitor, monitorId)
    bar.show_all()
    bars.append(bar)

display = Gdk.Display.get_default()

def generateBars():
    for bar in bars: # loop through bars
        bar.hide()
        del bar # and dispose of them

    for monitorNumber in range(Gdk.Display.get_n_monitors(display)): # loop through monitors
        newBar(Gdk.Display.get_monitor(display, monitorNumber), monitorNumber) # and create a bar for them

display.connect("monitor-added", lambda _, _2: generateBars())
display.connect("monitor-removed", lambda _, _2: generateBars())

generateBars()

# === RUN ===

helpers.setStylesheet("style.css")

Gtk.main()
