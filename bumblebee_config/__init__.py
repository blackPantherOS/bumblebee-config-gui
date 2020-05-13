# -*- coding: utf-8 -*-

"""
@author: Charles K Barcza (blackPanter OS) and old python2:Alessandro Facciorusso
"""

import os
import locale
import gettext

from bumblebee_config.utils import determine_module_path

APP = "bumblebee-config-gtk"
LOCALE_DIR = os.path.join(determine_module_path(), "l10n")

locale.setlocale(locale.LC_ALL, '')
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
