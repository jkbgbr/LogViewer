# -*- coding: utf-8 -*-
"""
log definitions
"""

pnp = {'entry_structure': ('Timestamp', 'Session', 'emitter', 'Level', 'message'),
       'separator': ' -- ',
       'name': 'PyNozzlePro',
       'logdir_path': 'V:\\KO\\NozzlePro'}

wss = {'entry_structure': ('Timestamp', 'Session', 'Level', 'message'),
       'separator': ' -- ',
       'name': 'Wasserstrahlschneider',
       'logdir_path': 'W:\\GJ\\Logs\\WSS'}

#
# vw = {'entry_structure': ('Timestamp', 'Session', 'Level', 'emitter', 'module', 'line', 'method', 'message'),
#       'separator': ' ++ ',
#       'name': 'VW',
#       'logdir_path': 'C:\\Users\\Jakab Gábor\\AppData\\Roaming\\LogViewer\\Logs'}

# vw = {'entry_structure': ('Timestamp', 'Session', 'Level', 'emitter', 'module', 'line', 'method', 'message'),
#       'separator': ' ++ ',
#       'name': 'VW',
#       'logdir_path': 'C:\\Users\\Jakab Gábor\\AppData\\Roaming\\LogViewer\\Logs'}

logdefinitions = wss, pnp
