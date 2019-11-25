# -*- coding: utf-8 -*-
"""
log definitions
"""

# pnp = {'entry_structure': ('Timestamp', 'Session', 'Level', 'emitter', 'module', 'line', 'method', 'message'),
#        'separator': ' -- ',
#        'name': 'PNP',
#        'directory_path': 'C:\\Users\\Jakab Gábor\\AppData\\Roaming\\LogViewer\\Logs'}
#
# vw = {'entry_structure': ('Timestamp', 'Session', 'Level', 'emitter', 'module', 'line', 'method', 'message'),
#       'separator': ' ++ ',
#       'name': 'VW',
#       'directory_path': 'C:\\Users\\Jakab Gábor\\AppData\\Roaming\\LogViewer\\Logs'}

wss = {'entry_structure': ('Timestamp', 'Level', 'message'),
       'separator': ' -- ',
       'name': 'WSS',
       'directory_path': 'W:\\DI-Wasserstrahlschneiden\\Programzettel%20Aktuell\\log.txt'}

vw = {'entry_structure': ('Timestamp', 'Session', 'Level', 'emitter', 'module', 'line', 'method', 'message'),
      'separator': ' ++ ',
      'name': 'VW',
      'directory_path': 'C:\\Users\\Jakab Gábor\\AppData\\Roaming\\LogViewer\\Logs'}

logdefinitions = ws, vw
