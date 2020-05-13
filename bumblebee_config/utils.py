# -*- coding: utf-8 -*-

"""
@author: Charles K Barcza (blackPanter OS) and old python2:Alessandro Facciorusso
"""

import os


def determine_module_path():
    try:
        root = __file__

        if os.path.islink(root):
            root = os.path.realpath(root)
        return os.path.dirname(os.path.abspath(root))
    except:
        raise SystemError("Could not find the __file__ var. Exiting.")
        sys.exit()
