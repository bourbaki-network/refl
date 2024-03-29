#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
from os.path import expanduser

HOME = expanduser("~")
ROOT = path.join(HOME, '.refl')

LOGGING = HOME
LOGFILE = 'refl.log'
LOGLEVEL = 'info'
