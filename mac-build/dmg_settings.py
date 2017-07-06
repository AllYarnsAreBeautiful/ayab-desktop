# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import biplist
import os.path

application = defines.get('app', '../dist/AYAB-Launcher.app')
appname = os.path.basename(application)
format = defines.get('format', 'UDBZ')
size = defines.get('size', None)
files = [ application ]
symlinks = { 'Applications': '/Applications' }
icon_locations = {
    appname:        (140, 90),
    'Applications': (500, 90)
    }
background = 'builtin-arrow'
#background = None
show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False
sidebar_width = 180
window_rect = ((100, 100), (640, 280))
default_view = 'icon-view'
show_icon_preview = False
arrange_by = None
grid_offset = (0, 0)
grid_spacing = 100
scroll_position = (0, 0)
label_pos = 'bottom' # or 'right'
text_size = 16
icon_size = 128

