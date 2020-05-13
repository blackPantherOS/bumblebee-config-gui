#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author: Charles K Barcza (blackPanter OS) and old python2:Alessandro Facciorusso
"""

bumblebeeConfFile = "/etc/bumblebee/bumblebee.conf"

bumblebeeConfSchema = """
# Configuration file for Bumblebee. Values should **not** be put between quotes

## Server options. Any change made in this section will need a server restart
# to take effect.
[bumblebeed]
# The secondary Xorg server DISPLAY number
VirtualDisplay={0[bumblebeed][VirtualDisplay]}
# Should the unused Xorg server be kept running? Set this to true if waiting
# for X to be ready is too long and don't need power management at all.
KeepUnusedXServer={0[bumblebeed][KeepUnusedXServer]}
# The name of the Bumbleblee server group name (GID name)
ServerGroup={0[bumblebeed][ServerGroup]}
# Card power state at exit. Set to false if the card shoud be ON when Bumblebee
# server exits.
TurnCardOffAtExit={0[bumblebeed][TurnCardOffAtExit]}
# The default behavior of '-f' option on optirun. If set to "true", '-f' will
# be ignored.
NoEcoModeOverride={0[bumblebeed][NoEcoModeOverride]}
# The Driver used by Bumblebee server. If this value is not set (or empty),
# auto-detection is performed. The available drivers are nvidia and nouveau
# (See also the driver-specific sections below)
Driver={0[bumblebeed][Driver]}
# Directory with a dummy config file to pass as a -configdir to secondary X
XorgConfDir={0[bumblebeed][XorgConfDir]}

## Client options. Will take effect on the next optirun executed.
[optirun]
# Acceleration/ rendering bridge, possible values are auto, virtualgl and
# primus.
Bridge={0[optirun][Bridge]}
# The method used for VirtualGL to transport frames between X servers.
# Possible values are proxy, jpeg, rgb, xv and yuv.
VGLTransport={0[optirun][VGLTransport]}
# List of paths which are searched for the primus libGL.so.1 when using
# the primus bridge
PrimusLibraryPath={0[optirun][PrimusLibraryPath]}
# Should the program run under optirun even if Bumblebee server or nvidia card
# is not available?
AllowFallbackToIGC={0[optirun][AllowFallbackToIGC]}


# Driver-specific settings are grouped under [driver-NAME]. The sections are
# parsed if the Driver setting in [bumblebeed] is set to NAME (or if auto-
# detection resolves to NAME).
# PMMethod: method to use for saving power by disabling the nvidia card, valid
# values are: auto - automatically detect which PM method to use
#         bbswitch - new in BB 3, recommended if available
#       switcheroo - vga_switcheroo method, use at your own risk
#             none - disable PM completely
# https://github.com/Bumblebee-Project/Bumblebee/wiki/Comparison-of-PM-methods

## Section with nvidia driver specific options, only parsed if Driver=nvidia
[driver-nvidia]
# Module name to load, defaults to Driver if empty or unset
KernelDriver={0[driver-nvidia][KernelDriver]}
PMMethod={0[driver-nvidia][PMMethod]}
# colon-separated path to the nvidia libraries
LibraryPath={0[driver-nvidia][LibraryPath]}
# comma-separated path of the directory containing nvidia_drv.so and the
# default Xorg modules path
XorgModulePath={0[driver-nvidia][XorgModulePath]}
XorgConfFile={0[driver-nvidia][XorgConfFile]}

## Section with nouveau driver specific options, only parsed if Driver=nouveau
[driver-nouveau]
KernelDriver={0[driver-nouveau][KernelDriver]}
PMMethod={0[driver-nouveau][PMMethod]}
XorgConfFile={0[driver-nouveau][XorgConfFile]}
"""

import configparser as ConfigParser
from gettext import gettext as _


class Settings(dict):

    """docstring for Settings"""
    def __init__(self):
        super(Settings, self).__init__()

        self["bumblebeed"] = {"VirtualDisplay": ":8", "KeepUnusedXServer": "false",
                              "ServerGroup": "bumblebee", "TurnCardOffAtExit": "false", "NoEcoModeOverride": "false", "Driver": "", "XorgConfDir": "/etc/bumblebee/xorg.conf.d"}
        self["optirun"] = {"Bridge": "auto", "VGLTransport": "proxy", "PrimusLibraryPath": "/usr/lib/x86_64-linux-gnu/primus:/usr/lib/i386-linux-gnu/primus", "AllowFallbackToIGC": "false"}
        self[
            "driver-nvidia"] = {"KernelDriver": "nvidia-current", "PMMethod": "auto", "LibraryPath": "/usr/lib/nvidia-current:/usr/lib32/nvidia-current",
                                "XorgModulePath": "/usr/lib/nvidia-current/xorg,/usr/lib/xorg/modules", "XorgConfFile": "/etc/bumblebee/xorg.conf.nvidia"}
        self["driver-nouveau"] = {
            "KernelDriver": "nouveau", "PMMethod": "auto", "XorgConfFile": "/etc/bumblebee/xorg.conf.nouveau"}

        self.loadSettings()

    def saveSettings(self):
        with open(bumblebeeConfFile, "w") as confFile:
            confFile.write(self.getCompiledConfFile())

    def loadSettings(self):
        configParser = ConfigParser.ConfigParser()
        configParser.optionxform = str
        configParser.read(bumblebeeConfFile)

        bumblebeedConfKeys = []
        optirunConfKeys = []
        nvidiaConfKeys = []
        nouveauConfKeys = []

        for section in self.keys():
            for key in self[section].keys():
                try:
                    self[section][key] = configParser.get(section, key)
                except:
                    pass

    def getCompiledConfFile(self):
        return bumblebeeConfSchema.format(self)
