# -*- coding: utf-8 -*-
"""
log definitions

Dictionaries defining the properties of the logs to be shown by the app

entry_structure: names corresponding the fields in the log entries. This is used to parse the messages and
serve as column names for the logs viewer

separator: the string used to separate the fields. Should be unambiguous

section_start: for the case the log contains multiple sections. e.g. the app logs the startup process thus there
are entries that come only once. If defined, the occurrancies will be counted.

name: the name of the log. Will be shown in the tree on the left of the GUI

default_level: if other than None, this level will be shown automatically when a log of this type is opened

logdir_path: path to the directory the logs are to be found. This will be searched and all files that can be parsed
will be shown in the tree view.

"""

# -*- coding: utf-8 -*-
"""
log definitions
"""

pnp = {'entry_structure': ('Timestamp', 'Session', 'emitter', 'Level', 'message'),
       'separator': ' -- ',
       'section_start': 'Program start',
       'name': 'PyNozzlePro',
       'default_level': 'INFO',
       'logdir_path': 'V:\\KO\\NozzlePro'}

pyTVRG_sim = {'entry_structure': ('Timestamp', 'emitter', 'Level', 'message'),
              'separator': '|',
              'name': 'tvrg data simulator',
              'section_start': 'Program start',
              'default_level': 'DEBUG',
              'logdir_path': 'E:\\Tiszavirag\\pyTVRG\\monitoring\\simulator'}

pyTVRG = {'entry_structure': ('Timestamp', 'Level', 'module', 'message'),
          'separator': '|',
          'section_start': 'Started pyTVRG',
          'name': 'pyTVRG',
          'default_level': 'DEBUG',
          'logdir_path': 'C:\\Users\\Jakab Gábor\\AppData\\Roaming\\pyTVRG\\Logs'}

pyTVRG_trace = {'entry_structure': ('Timestamp', 'Level', 'emitter', 'module', 'line', 'function', 'message'),
                'separator': ' -- ',
                'section_start': 'Started pyTVRG',
                'name': 'tvrg trace',
                'default_level': 'DEBUG',
                'logdir_path': 'C:\\Users\\Jakab Gábor\\AppData\\Roaming\\pyTVRG\\Logs'}

wss = {'entry_structure': ('Timestamp', 'Session', 'Level', 'message'),
       'separator': ' -- ',
       'section_start': 'STARTING',
       'name': 'Wasserstrahlschneider',
       'default_level': None,
       'logdir_path': 'W:\\GJ\\Logs\\WSS'}

logdefinitions = wss, pnp, pyTVRG, pyTVRG_sim, pyTVRG_trace
