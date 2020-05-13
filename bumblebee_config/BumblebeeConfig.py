#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author: Charles K Barcza (blackPanter OS) and old python2:Alessandro Facciorusso
"""

from gi.repository import Gtk
import os
import sys
import pkg_resources
from gettext import gettext as _

from bumblebee_config.Settings import Settings
from bumblebee_config.utils import determine_module_path
from bumblebee_config import BumblebeeHelper


APP = "bumblebee-config-gtk"

try:
    __version__ = pkg_resources.require(APP)[0].version
except:
    __version__ = ""


class BumblebeeConfig(object):

    def __init__(self):
        super(BumblebeeConfig, self).__init__()

        self.widgetList = []

        # widget, type, section, key
        # for radio only the first
        self.widgetsMap = [
            ["virtDispEntry", "entry", "bumblebeed", "VirtualDisplay"],
            ["keepUnusServerRadio1", "radio", "bumblebeed", "KeepUnusedXServer"],
            ["serverGroupEntry", "entry", "bumblebeed", "ServerGroup"],
            ["turnCardOffRadio1", "radio", "bumblebeed", "TurnCardOffAtExit"],
            ["noEcoModeRadio1", "radio", "bumblebeed", "NoEcoModeOverride"],
            ["driverComboBox", "cbbox", "bumblebeed", "Driver"],
            ["xorgConfDirEntry", "entry", "bumblebeed", "XorgConfDir"],

            ["bridgeComboBox", "cbbox", "optirun", "Bridge"],
            ["vglTransportComboBox", "cbbox", "optirun", "VGLTransport"],
            ["primusLibraryPathEntry", "entry", "optirun", "PrimusLibraryPath"],
            ["allowFallbackToIgcRadio1", "radio", "optirun", "AllowFallbackToIGC"],

            ["kernelDriverNvidiaEntry", "entry", "driver-nvidia", "KernelDriver"],
            ["pmMethodNvidiaComboBox", "cbbox", "driver-nvidia", "PMMethod"],
            ["libraryPathEntry", "entry", "driver-nvidia", "LibraryPath"],
            ["xorgModulePathEntry", "entry", "driver-nvidia", "XorgModulePath"],
            ["xorgConfFileNvidiaEntry", "entry", "driver-nvidia", "XorgConfFile"],

            ["kernelDriverNouveauEntry", "entry", "driver-nouveau", "KernelDriver"],
            ["pmMethodNouveauComboBox", "cbbox", "driver-nouveau", "PMMethod"],
            ["xorgConfFileNouveauEntry", "entry", "driver-nouveau", "XorgConfFile"]
        ]

        self.settings = Settings()

        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(APP)
        self.builder.add_from_file(os.path.join(determine_module_path(), "conf_window.ui"))

        self.mainWindow = self.builder.get_object("window1")
        self.mainWindow.set_title(_("Bumblebee Configurator GUI") + " " + __version__)

        self.builder.get_object("saveToolButton").connect("clicked", self._updateAndSaveSettings)

        for name, widgetType, section, key in self.widgetsMap:
            self.widgetList.append([self.builder.get_object(name), widgetType, section, key])

        self._updateWidgets()

    def _updateAndSaveSettings(self, widget):
        self.settings.saveSettings()

        msg = ""
        msg += _("Executing \'services bumblebeed restart\':") + "\n"
        msg += BumblebeeHelper.restartBumblebeed()
        msg += "\n" + _("Checking bumblebeed status:") + "\n"
        msg += BumblebeeHelper.checkBumblebeedStatus()

        dialog = Gtk.MessageDialog(self.mainWindow, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, _("Bumblebee output"))
        dialog.format_secondary_text(msg)
        dialog.run()
        dialog.destroy()
        print (msg)
        print(_("Settings saved."))

    def _onRadioChanged(self, widget, data):
        (section, key) = data
        if widget.get_active():
            value = "true"
        else:
            value = "false"
        self.settings[section][key] = value

    def _onEntryChanged(self, widget, data):
        (section, key) = data
        self.settings[section][key] = widget.get_text()

    def _onCbboxChanged(self, widget, data):
        (section, key) = data
        self.settings[section][key] = widget.get_active_text().lower()

    def _updateWidgets(self):
        for widget, widgetType, section, key in self.widgetList:
            if widgetType == "entry":
                widget.set_text(self.settings[section][key])
                widget.connect("changed", self._onEntryChanged, [section, key])
            elif widgetType == "radio":
                group = widget.get_group()
                for el in group:
                    if self.settings[section][key].lower() == "true" and el == widget:
                        widget.set_active(True)
                        break
                    elif self.settings[section][key].lower() == "false" and el != widget:
                        el.set_active(True)
                        break

                widget.connect("toggled", self._onRadioChanged, [section, key])
            elif widgetType == "cbbox":
                model = widget.get_model()
                i = 0
                for el in model:
                    el1 = el[0]
                    if self.settings[section][key] == "":
                        widget.set_active(0)
                        break
                    else:
                        if self.settings[section][key] == el1.lower():
                            widget.set_active(i)
                            break

                    i += 1
                widget.connect("changed", self._onCbboxChanged, [section, key])

    def _hideMe(self, widget):
        self.mainWindow.hide()

    def runAsDialog(self, parent):
        self.mainWindow.set_transient_for(parent)
        self.mainWindow.set_modal(True)
        self.mainWindow.connect("delete-event", lambda x,y: self._hideMe(x))
        self.builder.get_object("quitToolButton").connect("clicked", self._hideMe)
        self.mainWindow.show_all()

    def run(self):
        self.mainWindow.connect("delete-event", Gtk.main_quit)
        self.builder.get_object("quitToolButton").connect("clicked", Gtk.main_quit)
        self.mainWindow.show_all()
        Gtk.main()
