#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ayab
from sys import platform

# Check if we're on OS X, first.
if platform == 'darwin':
    from Foundation import NSBundle
    bundle = NSBundle.mainBundle()
    if bundle:
        info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
        if info and info['CFBundleName'] == 'Python':
            info['CFBundleName'] = 'AYAB'

ayab.run()
