# -*- coding: utf-8 -*-
"""
config data
"""

import os

APP_NAME = 'LW'
APP_LONG_NAME = 'LogViewer'
CONFIGFILE_NAME = '{}_Config'.format(APP_NAME)  # the config die is set when the app is initialized

if os.name == 'nt':
    LOGGING_DIR = os.path.join(os.getenv('APPDATA'), APP_LONG_NAME, 'Logs')
    CONFIG_DIR = os.path.join(os.getenv('APPDATA'), APP_LONG_NAME)
elif os.name == 'posix':
    LOGGING_DIR = os.path.join('~/.%s' % APP_LONG_NAME, 'Logs')
    CONFIG_DIR = os.path.join('~/.%s' % APP_LONG_NAME)
else:
    raise Exception('Unknown OS type')

LOGLEVELS = ('TRACE', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')  # used in the log window for filtering

CONFIGFILE_PATH = os.path.join(CONFIG_DIR, CONFIGFILE_NAME)

UNDEFINED = '!!!'  # the string put in the list if the log entry is not long enough. Happens if the log message is empty

# colors for the log levels in the log window
log_level_colors = {
    'DEBUG': (255, 255, 255),  # white
    'INFO': (250, 250, 250),  # bit lighter as light grey
    'WARNING': (255, 200, 0),  # yellow
    'ERROR': (255, 120, 0),  # light red
    'CRITICAL': (255, 40, 0),  # darker red
}