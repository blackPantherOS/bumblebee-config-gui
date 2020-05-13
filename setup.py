#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author: Charles K Barcza (blackPanther OS) the Python3 version. Python2 release Alessandro Facciorusso
"""

from distutils.core import setup
from glob import glob

PKG_NAME = "bumblebee_config"

pkg_data = {PKG_NAME: ["*.ui", "l10n/*/*/*"]}

other_files = [("/usr/share/applications", ["bumblebee-config.desktop"]), ("/usr/share/icons", ["img/bumblebee-config.png"])]


setup(name="bumblebee-config-gtk",
      version="0.7.0",
      author="Charles K Barcza",
      author_email='info@blackpanther.hu',
      url='https://github.com/blackPantherOS/bumblebee-config-gui',
      license="GNU General Public License (GPL3)",
      packages=[PKG_NAME],
      package_data=pkg_data,
      data_files=other_files,
      scripts=["bumblebee-config"]
      )
