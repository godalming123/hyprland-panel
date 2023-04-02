#!/usr/bin/env python3

# === IMPORTS ===

import gi
import time

import helpers

gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')

from gi.repository import Gtk, GtkLayerShell, GLib, Gdk

# === WIDGETS ===

def seperator():
    return Gtk.Label(justify=Gtk.Justification.CENTER, label="-")

def timeBtn(onclick):
    btn = Gtk.Button()
    btn.connect("clicked", onclick)
    
    def updateTime():
        theTime = time.localtime(time.time())
        btn.set_label(str(theTime.tm_hour%12).zfill(2) + "\n" + str(theTime.tm_min).zfill(2))
        return True
    
    if updateTime():
        GLib.timeout_add(15*1000, updateTime)
        return btn

# def hoverRevealer(icon, progress, onChange):
#     # === TODO ===
#     revealer = Gtk.Revealer()
#     revealer.set_reveal_child(Gtk.Label(label="hi"))

def batteryInformation():
    progress = Gtk.ProgressBar(
        orientation=Gtk.Orientation.VERTICAL,
        halign=Gtk.Align.CENTER,
        inverted=True
    )
    text = Gtk.Label(justify=Gtk.Justification.CENTER);

    def updateInfo():
        batInfo = helpers.getBattery()
        if not batInfo["error"]:
            Gtk.ProgressBar.set_fraction(progress, batInfo["charge"])

            if batInfo == "Charging\n":
                text.set_label("🔋↑")
            elif batInfo == "Full\n" or batInfo == "Not charging\n":
                text.set_label("🔋○")
            else:
                text.set_label("🔋↓")

            return True

    if updateInfo():
        GLib.timeout_add(30*1000, updateInfo)
        return progress, text

def workspacesWidget(monitorId):
    text = Gtk.Label(justify=Gtk.Justification.CENTER);

    def updateWorkspaces():
        monitors = helpers.getMonitors()
        workspaces = helpers.getWorkspaces()

        if workspaces != []: # if we got workspaces information
            workspacesText = ""
            if monitors != []: # if we got monitors information
                for monitor in monitors: # loop through monitors
                    if monitor["id"] == monitorId: # if monitor is the one we want
                        for workspace in workspaces: # then loop through workspaces
                            if workspace["monitor"] == monitor["name"]: # and if the workspace is on the monitor
                                # add it to the text
                                isActive = (monitor["activeWorkspace"]["id"] == workspace["id"])
                                if isActive:
                                    workspacesText += "❱ "
                                workspacesText += workspace["name"]
                                if isActive:
                                    workspacesText += " ❰"
                                workspacesText += "\n"
            else:
                for workspace in workspaces:
                    workspacesText += workspace["name"]
                    workspacesText += "\n"
            text.set_label(workspacesText) # set the text of the workspaces widget
            return True
    
    if updateWorkspaces():
        GLib.timeout_add(250, updateWorkspaces)
        return text

# === WINDOWS ===

launcher   = helpers.layeredWindow("launcher", Gtk.Label(label="Launcher!")) # TODO
background = helpers.layeredWindow("background", Gtk.Label(label="Background!"), "tlbr", "", GtkLayerShell.Layer.BACKGROUND) # TODO
datemenu   = helpers.layeredWindow("datemenu", Gtk.Calendar(), "br", "br")

def makeBar(monitor, monitorId):
    # search button
    searchBtn = Gtk.Button(label="⌥")
    searchBtn.connect("clicked", lambda _: helpers.toggleWindow(launcher))
    helpers.addClass(searchBtn, "search")

    # battery information
    batteryStatus = batteryInformation();

    box = helpers.newBox(
        Gtk.Orientation.VERTICAL,
        1,
        ["bar"],
        [searchBtn],
        workspacesWidget(monitorId),
        [timeBtn(lambda _: helpers.toggleWindow(datemenu))] + [batteryStatus[0], batteryStatus[1]] if batteryStatus else []
    )
    return helpers.layeredWindow("bar", box, "tlb", "tlbr", GtkLayerShell.Layer.TOP, True, monitor)

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
