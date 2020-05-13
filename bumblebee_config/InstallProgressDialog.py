#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author: Charles K Barcza (blackPanter OS) and old python2:Alessandro Facciorusso
"""

from gi.repository import Gtk
from gettext import gettext as _


class InstallProgressDialog(Gtk.Dialog):

    """A dialog for Progress of installation of bumblebee."""
    def __init__(self, parent):
        GObject.GObject.__init__(self, _("Bumblebee is installing..."), parent, Gtk.DialogFlags.MODAL,
                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        self.progress = 0.0

        self.set_default_size(350, -1)
        self.set_deletable(False)

        button = self.get_widget_for_response(Gtk.ResponseType.CANCEL)
        button.set_sensitive(False)

        self.mainLayout = Gtk.Box(homogeneous=True, orientation=Gtk.Orientation.VERTICAL)
        self.get_content_area().add(self.mainLayout)

        self.label = Gtk.Label()
        self.mainLayout.pack_start(self.label, False, False, 0)

        self.progressBar = Gtk.ProgressBar()
        self.mainLayout.pack_start(self.progressBar, True, False, 0)
        self.show_all()

    def setMessage(self, message):
        self.label.set_text(message)

    def setProgress(self, percent=None):
        if percent == None:
            self.progressBar.pulse()
        else:
            self.progress = percent
            self.progressBar.set_fraction(percent / 100)

    def getProgress(self):
        return self.progress

    def downloadingCb(self, percent):
        self.setMessage(_("Downloading files..."))
        self.setProgress(percent)

    def installingCb(self, msg, percent):
        if msg != "__FINISHED__":
            self.setMessage(msg)
            self.setProgress(percent)
        else:
            self.hide()
