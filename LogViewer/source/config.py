
import os

APP_NAME = 'LW'
APP_LONG_NAME = 'LogViewer'
CONFIGFILE_NAME = '{}_Config'.format(APP_NAME)  # the config die is set when the app is initialized

if os.name == 'nt':
    LOGGING_DIR = os.path.join(os.getenv('APPDATA'), APP_NAME, 'Logs')
    CONFIG_DIR = os.path.join(os.getenv('APPDATA'), APP_NAME)
elif os.name == 'posix':
    LOGGING_DIR = os.path.join('~/.%s' % APP_NAME, 'Logs')
    CONFIG_DIR = os.path.join('~/.%s' % APP_NAME)
else:
    raise Exception('Unknown OS type')

LOGLEVELS = ('TRACE', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')  # used in the log window for filtering

CONFIGFILE_PATH = os.path.join(CONFIG_DIR, CONFIGFILE_NAME)