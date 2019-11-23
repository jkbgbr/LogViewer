

import wx

import logging

import wx.lib.agw.aui as aui
import wx.lib.agw.persist as PM
import wx.lib.inspection
import wx.lib.mixins.inspection
# from pubsub import pub

from LogViewer.source.config import APP_LONG_NAME, CONFIGFILE_PATH, APP_NAME


logger = logging.getLogger('gui')


class MainFrame(wx.Frame):

    def __init__(self, parent, id=wx.ID_ANY, title='', pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER |
                                            wx.CLIP_CHILDREN | wx.NO_FULL_REPAINT_ON_RESIZE,
                 *args, **kwargs):

        self.window_title = {}  # title will be set based on manufacturer, customer info
        self.proposed_filename_data = {}  # a dict holding the info for a proposed file name
        self.appConfig = None  # the full config
        self.locale = None

        wx.Frame.__init__(self, parent, id, title, pos, size, style, *args, **kwargs)

        # reading the config an applying it
        self.SetName(APP_LONG_NAME)

        # controls that will be defined later
        self.treeview = None
        self.levellist = None
        self.logpanel = None

        # setting up the window
        self.SetMinSize((640, 480))
        self.Centre(wx.BOTH)
        self.pnl = wx.Panel(self)

        # # layout manager, tell FrameManager to manage this frame
        # self._mgr = aui.AuiManager()
        # self._mgr.SetManagedWindow(self.pnl)
        #
        # # persistence
        # # for now this only stores
        # self._persistMgr = PM.PersistenceManager.Get()  # define the manager
        # self._persistMgr.SetPersistenceFile(CONFIGFILE_PATH)
        # if not self._persistMgr.RegisterAndRestoreAll(self):
        #     pass

        # menubar and main menu points
        self.menubar = None
        self.file_menu = None

        # creating the main components of the GUI
        self.BuildMenuBar()  # menubar
        # self.BuildTreeView()  # the view listing available files
        # self.BuildLevelLister()  # the list of available levels
        # self.BuildLogWindow()  # the lower panel for logging

        # sizers and stuff

        # boxes
        mainsizer = wx.BoxSizer(wx.HORIZONTAL)

        # rightBox = wx.BoxSizer(wx.VERTICAL)
        # mainsizer.Add(rightBox)

        self.splitter = wx.SplitterWindow(self, -1)
        leftBox = wx.BoxSizer(wx.VERTICAL)
        leftBox.Add(self.splitter, 1, wx.EXPAND)
        mainsizer.Add(leftBox)

        self.treePanel = wx.Panel(self.splitter, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN)
        # self.treeview = wx.TreeCtrl(parent=self.treePanel)
        # leftBox.Add(self.treeview, 1, wx.EXPAND)
        # self.treePanel.SetSizerAndFit(leftBox)

        # self.listerPanel = wx.Panel(self.splitter)
        # self.treeview = wx.TreeCtrl(parent=self.treePanel)
        # leftBox.Add(self.treeview, 1, wx.EXPAND)
        # self.treePanel.SetSizerAndFit(leftBox)
        # #
        # # self.listerPanel = wx.Panel(self.splitter)
        # # self.levellist = wx.ListView(self.listerPanel)
        # # leftBox.Add(self.levellist, 1, wx.EXPAND)
        # # self.levellist.SetSizerAndFit(leftBox)
        # # self.splitter.SplitHorizontally(self.treePanel, self.listerPanel)
        # # self.listerPanel.SetSizerAndFit(leftBox)
        #
        # # Use the aui manager to set up everything
        # # self._mgr.AddPane(self.centerPanel, aui.AuiPaneInfo().Layer(1).Center().Name('notebook').
        # #                   Floatable(False).Gripper(False).
        # #                   CloseButton(False).MinSize((640, 80)))
        # # self._mgr.AddPane(self.treePanel, aui.AuiPaneInfo().Layer(1).
        # #                   Left().BestSize((200, -1)). MinSize((100, -1)).Caption('Logs').
        # #                   Floatable(False).CloseButton(False).Name('tree'))
        # # self._mgr.AddPane(self.logpanel,
        # #                   aui.AuiPaneInfo().GripperTop(False).Bottom().BestSize((-1, 900)).Layer(0).MinSize((-1, 100)).
        # #                   Floatable(False).CloseButton(False).MinimizeButton(False).
        # #                   MinimizeMode(aui.AUI_MINIMIZE_POS_BOTTOM).Name('logwindow').Caption('Log window'))
        # # self._mgr.Update()
        # # self.default_layout = self._mgr.SavePerspective()  # saving the default layout

        # AppConfig stuff
        self.appConfig = wx.FileConfig(appName=APP_NAME,
                                       vendorName='JakabGabor',
                                       localFilename=CONFIGFILE_PATH)

        # sending out a message telling init is finished
        logger.debug('Config file name set to {}'.format(self.appConfig.GetLocalFileName(APP_NAME)))

    def BuildMenuBar(self):
        """
        Bilds the menu bar.

        :return:
        """
        self.menubar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.menubar.Append(self.file_menu, '&File')

        # finally after having defined it: setting the menu bar
        self.SetMenuBar(self.menubar)

    # def BuildTreeView(self):
    #     self.treePanel = wx.Panel(self.pnl, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN)
    #     self.treeview = wx.TreeCtrl(parent=self.treePanel)
    #
    # def BuildLevelLister(self):
    #     self.listerPanel = wx.Panel(self.pnl, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN)
    #     self.levellist = wx.ListView(self.pnl)

    # def BuildLogWindow(self):
    #     pass

if __name__ == '__main__':

    from LogViewer.source.main import App
    app = App()
    app.start()

    frame = MainFrame(None)