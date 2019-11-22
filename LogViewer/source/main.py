# -*- coding: utf-8 -*-
"""
main.py for the package VW
"""

import wx

import logging
# from logging import config
# from VW.Logging.configuration import logger_config

from LogViewer.source.config import LOGGING_DIR, CONFIG_DIR
from LogViewer.source.controller import Controller
import os.path

# logging.config.dictConfig(logger_config)

# making sure the log and config directories exist:
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

# # creating the root loggers for this session
# logging.config.dictConfig(logger_config)

# as the GUI is not visible yet, logs will show up only in the log files
logger = logging.getLogger(__name__)


class App(wx.App):

    def __init__(self, redirect=False):
        # app = VW_App(redirect=True, filename='E:\logfile.log')
        super(App, self).__init__(redirect)
        self.controller = Controller()
        logger.debug('App initialized')

    def OnInit(self):  # added so we can have a nice splash screen
        wx.GetApp().Yield()  # allowing for processing pending events
        return True

    def start(self):
        self.SetTopWindow(self.controller.view)
        # wx.lib.inspection.InspectionTool().Show()
        self.controller.view.Show()
        self.MainLoop()


if __name__ == '__main__':  # pragma: no cover
    app = App()
    app.start()

#
#
# def main():
#     logger.debug('-' * 80)
#     logger.debug('*' * 80)
#     logger.debug('Starting a new session')
#     logger.debug('*' * 80)
#     logger.debug('-' * 80)
#     app = VW_App(redirect=False)
#     app.start()
#
#
# if __name__ == '__main__':  # pragma: no cover
#     main()
