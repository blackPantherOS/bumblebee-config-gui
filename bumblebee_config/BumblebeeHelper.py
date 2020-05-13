#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author: Charles K Barcza (blackPanter OS) and old python2:Alessandro Facciorusso
"""

import subprocess


def restartBumblebeed():
    output = ""
    process = subprocess.Popen("systemctl restart bumblebeed".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    output += stdout.decode()
    return output


def checkBumblebeedStatus():
    output = ""
    process = subprocess.Popen("bumblebeed -v".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    output += stderr.decode()

    return output
