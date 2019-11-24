

import wx
import wx.lib.inspection
import wx.lib.mixins.inspection
import wx.lib.mixins.listctrl as listmix
from pubsub import pub

from LogViewer.source.config import APP_LONG_NAME, CONFIGFILE_PATH, APP_NAME

# logger = logging.getLogger('gui')


ID_Menu_CustomerInfo = wx.ID_ANY


class MenuBar(wx.MenuBar):

    def __init__(self):
        super(MenuBar, self).__init__()
        self.file_menu = wx.Menu()
        self.Append(self.file_menu, '&File')

    def OnDescriptorChosen(self, event, clicked):
        print(clicked)


class HSplitterPanel(wx.Panel):
    """ Constructs a Horizontal splitter window with top and bottom panels"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        splitter = wx.SplitterWindow(self, style=wx.SP_3D | wx.SP_LIVE_UPDATE)
        self.TopPanel = wx.Panel(splitter)
        self.BottomPanel = wx.Panel(splitter)

        splitter.SplitHorizontally(self.TopPanel, self.BottomPanel)
        self.PanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.PanelSizer.Add(splitter, 1, wx.EXPAND | wx.ALL)

        self.SetSizer(self.PanelSizer)


class Tree(wx.TreeCtrl):

    def __init__(self, parent):
        # wx.TreeCtrl.__init__(self, parent, style=wx.TR_MULTIPLE | wx.TR_HAS_BUTTONS)
        wx.TreeCtrl.__init__(self, parent)
        self.tree = None

    def update_tree(self, treedata=None):

        self.DeleteAllItems()

        if treedata is not None:
            self.tree = treedata
            root = self.AddRoot('Logs')
            self.SetItemHasChildren(root, True)
            self.SetItemData(root, self.tree)

            self.Unbind(wx.EVT_TREE_ITEM_COLLAPSED)
            self.Unbind(wx.EVT_TREE_ITEM_EXPANDING)
            self.Unbind(wx.EVT_TREE_ITEM_RIGHT_CLICK)
            self.Unbind(wx.EVT_TREE_SEL_CHANGED)

            # Bind some interesting events
            self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self)
            self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding, self)
            # self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightClick, self)
            self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnLeftClick, self)
            self.CollapseAll()
            self.ExpandAll()

    def OnLeftClick(self, event):
        """
        when a tree node is left-clicked, we recreate the attribute selected_items that holds the selected items
        this is then pubsubbed so the relevant data can be shown at once
        """
        pub.sendMessage('tree.selected', data=self.GetItemData(event.GetItem()))

    def OnItemCollapsed(self, evt):
        # And remove them when collapsed as we don't need them any longer
        self.DeleteChildren(evt.GetItem())

    def OnItemExpanding(self, event):
        # When the item is about to be expanded add the first level of child nodes
        self.Freeze()
        treenode = event.GetItem()
        self.AddTreeNodes(treenode)
        self.Thaw()

    def AddTreeNodes(self, treenode):
        node = self.GetItemData(treenode)  # the ANYTREE node
        for child in node.children:
            _name = child.name
            newItem = self.AppendItem(treenode, _name, data=child)
            if child.children:
                self.SetItemHasChildren(newItem, True)


class LogList(wx.ListView, listmix.ListCtrlAutoWidthMixin):

    def __init__(self, parent):
        super(LogList, self).__init__(parent, winid=wx.ID_ANY,
                                      style=wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_HRULES | wx.LC_VRULES)
        self.log = None
        self.all_lines = None

    def build_columns(self, log=None):
        self.Freeze()
        self.ClearAll()
        for eindex, entry in enumerate(log.descriptor.entry_structure):
            self.InsertColumn(eindex, entry)
        self.Thaw()

    def OnGetItemText(self, item, column):
        return self.log.parse_entry(self.all_lines[item], separator=self.log.separator)[column]

    def fill_list(self, log=None):
        """reads the lines from the file and fills the listctrl"""
        self.log = log
        self.all_lines = log.read_logfile(logfile=log.logfile)
        self.build_columns(log)
        self.SetItemCount(len(self.all_lines))


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

        # # controls that will be defined later
        self.treectrl = None
        self.levellist = None
        self.loglist = None

        # setting up the window
        self.SetMinSize(size)
        self.Centre(wx.BOTH)

        # creating the main components of the GUI
        self.BuildMainStructure()  # splitters, panels
        self.sb = self.CreateStatusBar()

        # menu bar
        self.menubar = MenuBar()
        self.SetMenuBar(self.menubar)

        # AppConfig stuff
        self.appConfig = wx.FileConfig(appName=APP_NAME,
                                       vendorName='JakabGabor',
                                       localFilename=CONFIGFILE_PATH)

        # sending out a message telling init is finished
        # logger.debug('Config file name set to {}'.format(self.appConfig.GetLocalFileName(APP_NAME)))

    def BuildMainStructure(self):
        ################################################################
        # Define mainsplitter as child of Frame and add H and VSplitterPanel as children
        mainsplitter = wx.SplitterWindow(self, style=wx.SP_3D | wx.SP_LIVE_UPDATE)
        splitterpanel1 = HSplitterPanel(mainsplitter)

        right_panel = wx.Panel(mainsplitter)

        mainsplitter.SplitVertically(splitterpanel1, right_panel)
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        MainSizer.Add(mainsplitter, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(MainSizer)

        self.treectrl = Tree(splitterpanel1.TopPanel)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(self.treectrl, 1, wx.EXPAND)
        splitterpanel1.TopPanel.SetSizerAndFit(top_sizer)

        self.loglist = LogList(right_panel)

        right_sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_sizer.Add(self.loglist, 1, wx.EXPAND)
        right_panel.SetSizerAndFit(right_sizer)

        self.levellist = wx.TextCtrl(splitterpanel1.BottomPanel, style=wx.TE_MULTILINE)
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_sizer.Add(self.levellist, 1, wx.EXPAND)
        splitterpanel1.BottomPanel.SetSizerAndFit(bottom_sizer)


if __name__ == '__main__':

    from LogViewer.source.main import App
    app = App()
    app.start()

    frame = MainFrame(None)