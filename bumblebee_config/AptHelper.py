#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author: Charles K Barcza (blackPanter OS) and old python2:Alessandro Facciorusso
"""

import sys
import threading

from gi.repository import Gdk
from gettext import gettext as _

try:
#    import apt
    import rpm
    from softwareproperties.SoftwareProperties import SoftwareProperties
except:
    imported = False
#else:
#    imported = True
imported = False
apt = rpm

class UpdateFetchProgress(apt.progress.FetchProgress):

    def __init__(self, downloadCb):
        self.downloadCb = downloadCb

    def pulse(self):
        Gdk.threads_enter()
        self.downloadCb(self.percent)
        Gdk.threads_leave()

    def fail(self, data):
        pass


class TextInstallProgress(apt.progress.DumbInstallProgress):

    def __init__(self, installCb):
        super(TextInstallProgress, self).__init__()
        # print "inited TextInstallProgress"

        self.installCb = installCb
        self.last = 0.0

    def updateInterface(self):
        apt.progress.DumbInstallProgress.updateInterface(self)
        if self.last >= self.percent:
            return

        if self.percent == 100.0:
            Gdk.threads_enter()
            self.installCb(_("Configuring..."), None)
            Gdk.threads_leave()
        else:
            Gdk.threads_enter()
            self.installCb(self.status, self.percent)
            Gdk.threads_leave()
        self.last = self.percent


class InstallBumblebeeThread(threading.Thread):

    def __init__(self, downloadCb, installCb, removeFirst=False):
        super(InstallBumblebeeThread, self).__init__()
        self.downloadCb = downloadCb
        self.installCb = installCb
        self.removeFirst = removeFirst
        self.softProp = SoftwareProperties()

    def run(self):
        # print "Running InstallBumblebeeThread."
        cache = apt.Cache()

        if self.removeFirst:
            cache.open(None)
            cache['bumblebee'].markDelete()
            cache.commit(UpdateFetchProgress(self.downloadCb), TextInstallProgress(self.installCb))

        ppa = 'ppa:bumblebee/stable'
        uri = 'http://ppa.launchpad.net/bumblebee/stable/ubuntu'
        if uri not in [el.uri for el in self.softProp.get_isv_sources()]:
            # print "uri: %s" % uri
            self.softProp.add_source_from_line(ppa)
            self.softProp.sourceslist.save()
            try:
                cache.open(None)
                cache.update(UpdateFetchProgress(self.downloadCb))
            except apt.cache.FetchFailedException: 
                pass

        cache.open(None)
        cache['bumblebee'].markInstall()
        cache['bumblebee-nvidia'].markInstall()
        cache['linux-headers-generic'].markInstall()
        cache['primus'].markInstall()
        try:
            cache.commit(UpdateFetchProgress(self.downloadCb), TextInstallProgress(self.installCb))
        finally:
            Gdk.threads_enter()
            self.installCb("__FINISHED__", None)
            Gdk.threads_leave()


class AptHelper(object):

    def checkBumblebeeInstalled(self):
        if imported:
            cache = apt.Cache()

            res = False
            if cache['bumblebee'].isInstalled:
                res = True
            else:
                res = False
            return res

    """
        downloadCb: (percent)
        installCb: (msg, percent)
    """
    def installBumblebee(self, downloadCb, installCb, removeFirst=False):
        if imported:
            installThread = InstallBumblebeeThread(downloadCb, installCb, removeFirst)
            installThread.start()
