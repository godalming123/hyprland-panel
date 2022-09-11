#!/usr/bin/env python3

# === IMPORTS ===

import gi
import helpers
import time
import subprocess
import json

gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')

from gi.repository import Gtk, GtkLayerShell, GLib

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
    # === TODO ===
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
    return box

def workspacesWidget():
    text = Gtk.Label()
    Gtk.Label.set_justify(text, Gtk.Justification.CENTER)
    def updateWorkspaces():
        try:
            activeWindowWorkspaceId = json.loads(subprocess.check_output(["hyprctl", "activewindow", "-j"]))["workspace"]["id"]
        except:
            activeWindowWorkspaceId = None # there is no window active
        workspaces = json.loads(subprocess.check_output(["hyprctl", "workspaces", "-j"]))
        workspacesText = ""
        for workspace in workspaces:
            isActive = (activeWindowWorkspaceId == workspace["id"])
            if isActive:
                workspacesText += "("
            workspacesText += workspace["name"]
            if isActive:
                workspacesText += ")"
            workspacesText += "\n"
        text.set_label(workspacesText)
        return True
    
    updateWorkspaces()
    GLib.timeout_add(1000, updateWorkspaces)

    return text

# === WINDOWS ===

launcher   = helpers.layeredWindow("launcher", Gtk.Label(label="Launcher!")) # TODO
background = helpers.layeredWindow("background", Gtk.Label(label="Background!"), "tlbr", "", GtkLayerShell.Layer.BACKGROUND) # TODO
datemenu   = helpers.layeredWindow("datemenu", Gtk.Calendar(), "bl", "bl")

def makeBar():
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
    helpers.addClass(box, "bar-box")
    searchBtn = Gtk.Button(label="⌥")
    searchBtn.connect("clicked", lambda _: helpers.toggleWindow(launcher))
    helpers.addClass(searchBtn, "search")
    box.set_center_widget(workspacesWidget())
    box.pack_start(searchBtn, False, True, 0)
    box.pack_end(timeBtn(lambda _: helpers.toggleWindow(datemenu)), False, True, 0)
    return helpers.layeredWindow("bar", box, "tlb", "tlb", GtkLayerShell.Layer.TOP, True)

bar = makeBar()

# === RUN ===

helpers.setStylesheet("style.css")
bar.show_all()

Gtk.main()
