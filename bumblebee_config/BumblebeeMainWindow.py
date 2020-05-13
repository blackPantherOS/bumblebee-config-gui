#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author: Charles K Barcza (blackPanter OS) and old python2:Alessandro Facciorusso
"""

from gi.repository import Gtk, Gdk, GObject
import os
import sys
import platform
import pkg_resources

from gettext import gettext as _

from bumblebee_config.utils import determine_module_path
from bumblebee_config.BumblebeeConfig import BumblebeeConfig
from bumblebee_config import BumblebeeHelper
from bumblebee_config.InstallProgressDialog import InstallProgressDialog


APP = "bumblebee-config-gtk"
try:
    __version__ = pkg_resources.require(APP)[0].version
except:
    __version__ = ""


class BumblebeeMainWindow(object):

    def __init__(self):
        super(BumblebeeMainWindow, self).__init__()

        self.bumblebeeInstalled = False

#        self.aptHelper = AptHelper()

        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(APP)
        self.builder.add_from_file(os.path.join(determine_module_path(), "main_window.ui"))

        self.mainWindow = self.builder.get_object("window1")
        self.mainWindow.set_title(_("Bumblebee Configurator GUI") + " " + __version__)

        self.installButton = self.builder.get_object("installButton")
        self.installButton.connect("clicked", self._onInstallButtonClicked)
        self.builder.get_object("configureButton").connect("clicked", self._onConfigureButtonClicked)
        self.builder.get_object("restartButton").connect("clicked", self._onRestartButtonClicked)
        self.builder.get_object("checkStatusButton").connect("clicked", self._onCheckStatusButtonClicked)

        if self.isUbuntu():
    	    from bumblebee_config.AptHelper import AptHelper

        if self.isUbuntu():
            if self.aptHelper.checkBumblebeeInstalled():
                self.installButton.set_label(_("Reinstall Bumblebee"))
                self.bumblebeeInstalled = True
            else:
                self.installButton.set_label(_("Install Bumblebee"))
        else:
            self.installButton.set_sensitive(False)

    def isUbuntu(self):
        if platform.linux_distribution()[0].lower() == "ubuntu":
            return True
        else:
            return False

    def _onInstallButtonClicked(self, widget):
        dialog = InstallProgressDialog(self.mainWindow)
        self.aptHelper.installBumblebee(dialog.downloadingCb, dialog.installingCb, self.bumblebeeInstalled)
        dialog.run()
        dialog.destroy()
        self.installButton.set_label(_("Reinstall Bumblebee"))
        self.bumblebeeInstalled = True

    def _onConfigureButtonClicked(self, widget):
        confWnd = BumblebeeConfig()
        confWnd.runAsDialog(self.mainWindow)

    def _onRestartButtonClicked(self, widget):
        msg = ""
        msg += _("Executing \'services bumblebeed restart\':") + "\n"
        msg += BumblebeeHelper.restartBumblebeed()

        dialog = Gtk.MessageDialog(self.mainWindow, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, _("Bumblebee output"))
        dialog.format_secondary_text(msg)
        dialog.run()
        dialog.destroy()
        print (msg)

    def _onCheckStatusButtonClicked(self, widget):
        msg = ""
        msg += "\n" + _("Bumblebeed status:") + "\n"
        msg += BumblebeeHelper.checkBumblebeedStatus()

        dialog = Gtk.MessageDialog(self.mainWindow, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, _("Bumblebee output"))
        dialog.format_secondary_text(msg)
        dialog.run()
        dialog.destroy()
        print (msg)

    def run(self):    
        GObject.threads_init()
        Gdk.threads_init();
        Gdk.threads_enter();
        self.mainWindow.show_all()
        self.mainWindow.connect("delete-event", Gtk.main_quit)
        Gdk.threads_leave()
        Gtk.main()
        return 0
