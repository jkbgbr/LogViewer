# -*- coding: utf-8 -*-
"""
entry point
"""

# todo: reduce the number of uses and definitions of parse_entry
# todo: pre-parse all entries and use this to show, filter by level etc., so dummy entries are found as well

import os.path

import wx

from LogViewer.source.config import LOGGING_DIR, CONFIG_DIR
from LogViewer.source.controller import Controller

# from logging import config
# from VW.Logging.configuration import logger_config

# making sure the log and config directories exist:
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

# as the GUI is not visible yet, logs will show up only in the log files
# logger = logging.getLogger(__name__)


class LogViewerApp(wx.App):

    def __init__(self, redirect=False, external_logdefinition=None):
        super(LogViewerApp, self).__init__(redirect)
        self.controller = Controller(external_logdefinition)

    def OnInit(self):  # added so we can have a nice splash screen
        wx.GetApp().Yield()  # allowing for processing pending events
        return True

    def start(self):
        self.SetTopWindow(self.controller.view)
        # wx.lib.inspection.InspectionTool().Show()
        self.controller.view.Show()
        self.MainLoop()


if __name__ == '__main__':  # pragma: no cover
    # app = LogViewerApp()
    # app.start()

    VW = {'entry_structure': ('Timestamp', 'Session', 'Level', 'Emitter', 'File', 'Line', 'Method', 'Message'),
          'separator': ' -- ',
          'section_start': 'Starting a new session',
          'name': 'mimi',
          'default_level': 'TRACE',
          'logdir_path': os.path.abspath('C:\\Users\\Jakab Gábor\\AppData\\Roaming\\VW\\Logs')}

    logdefinitions = VW,

    app = LogViewerApp(external_logdefinition=logdefinitions)
    app.start()
