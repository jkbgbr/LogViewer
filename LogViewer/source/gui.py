# -*- coding: utf-8 -*-
"""
the view component
"""

import time
from typing import Set, Dict

import wx
import wx.lib.inspection
import wx.lib.mixins.inspection
import wx.lib.mixins.listctrl as listmix
from pubsub import pub

from LogViewer.source.config import APP_LONG_NAME, CONFIGFILE_PATH, APP_NAME, log_level_colors


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
        splitter.SetMinimumPaneSize(200)
        self.TopPanel = wx.Panel(splitter)
        self.BottomPanel = wx.Panel(splitter)

        splitter.SplitHorizontally(self.TopPanel, self.BottomPanel)
        self.PanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.PanelSizer.Add(splitter, 1, wx.EXPAND | wx.ALL)

        self.SetSizer(self.PanelSizer)


class Tree(wx.TreeCtrl):

    def __init__(self, parent):
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
            self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnLeftClick, self)
            self.CollapseAll()
            self.Expand(root)

    def OnLeftClick(self, event):
        pub.sendMessage('logviewer.tree.selected', log=self.GetItemData(event.GetItem()))

    def OnItemCollapsed(self, evt):
        self.DeleteChildren(evt.GetItem())

    def OnItemExpanding(self, event):
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


class Watch(wx.Timer):

    def __init__(self):
        super(Watch, self).__init__()
        self.Start(1000)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

    def OnTimer(self, event):
        # time string can have characters 0..9, -, period, or space
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pub.sendMessage('logviewer.time', time=ts)


class LogList(wx.ListView, listmix.ListCtrlAutoWidthMixin):

    def __init__(self, parent):
        super(LogList, self).__init__(parent, winid=wx.ID_ANY,
                                      style=wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_HRULES | wx.LC_VRULES)
        self.log = None
        self.all_lines = None

        # the background attribute to be set later
        # http://wxpython-users.1045709.n5.nabble.com/Changing-cell-background-inside-virtual-ListCtrl-td5720303.html
        self.backgroundcolor = wx.ListItemAttr()

        pub.subscribe(self.set_columns, 'logviewer.list.filled')
        pub.subscribe(self.fill_list, 'logviewer.list.filter')

    def set_log(self, log):
        self.log = log

    def clear_all(self):
        self.ClearAll()

    def build_columns(self, log=None):
        self.Freeze()
        self.ClearAll()

        for eindex, entry in enumerate(log.descriptor.entry_structure):
            self.InsertColumn(eindex, entry)
        self.Thaw()

    def OnGetItemAttr(self, item):
        """sets abd returns the background of the rows"""
        # extracting the level
        lvl = self.log.get_field_values(fieldname='level', lines=[self.all_lines[item]])
        # setting and returning
        self.backgroundcolor.SetBackgroundColour(self.colorizer(lvl.pop()))  # returns nothing, justs sets
        return self.backgroundcolor

    def OnGetItemText(self, item, column):
        """This is the method that makes the listctrl virtual"""
        _ret = self.log.parse_entry(self.all_lines[item], separator=self.log.separator,
                                    expected_length=self.log.descriptor.expected_length,
                                    level_position=self.log.descriptor.level_position)

        try:
            return _ret[column]
        except (IndexError, TypeError):
            print('Tried to access item {} in column {} with separator {}. Did not succeed.'.format(item, column,
                                                                                                    self.log.separator))
            print('The row to parse was: "{}"'.format(self.all_lines[item]))
            print('The parsed result is: "{}"'.format(_ret))

    def fill_list(self, level=None, emitter=None):
        """reads the lines from the file and fills the listctrl"""
        self.Freeze()
        lines = self.log.read_logfile(logfile=self.log.logfile)
        if level:
            lines = [x for x in lines if level in x]
        if emitter:
            lines = [x for x in lines if emitter in x]

        self.all_lines = lines
        self.build_columns(self.log)
        self.SetItemCount(len(lines))
        pub.sendMessage('logviewer.list.filled')
        self.Thaw()

    def colorize_entry(self, index, level):
        if index >= 0:
            self.SetItemBackgroundColour(index, self.colorizer(level))  # color

    @staticmethod
    def colorizer(level=None):
        return wx.Colour(log_level_colors.get(level, (155, 155, 155)))

    def set_columns(self):
        self.Freeze()
        for col in range(self.GetColumnCount()):
            self.SetColumnWidth(col, wx.LIST_AUTOSIZE_USEHEADER)
        self.Thaw()


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

        # reading the config and applying it
        self.SetName(APP_LONG_NAME)

        # # # controls that will be defined later
        self.treectrl = None
        self.levellist = None
        self.loglist = None
        self.settingspanel = None

        # setting up the window
        self.SetMinSize(size)
        self.Centre(wx.BOTH)

        # creating the main components of the GUI
        self.BuildMainStructure()  # splitters, panels
        self.sb = self.CreateStatusBar()

        # menu bar
        self.menubar = MenuBar()
        self.SetMenuBar(self.menubar)

        # timer watch
        self.watch = Watch()

        # AppConfig stuff
        self.appConfig = wx.FileConfig(appName=APP_NAME,
                                       vendorName='JakabGabor',
                                       localFilename=CONFIGFILE_PATH)

        # sending out a message telling init is finished
        # logger.debug('Config file name set to {}'.format(self.appConfig.GetLocalFileName(APP_NAME)))
        pub.subscribe(self.clear_all, 'logviewer.clear.all')
        pub.subscribe(self.show_logsummary, 'logviewer.statusbar.logsummary')
        pub.subscribe(self.set_time, 'logviewer.time')

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        pub.getDefaultTopicMgr().delTopic('logviewer')  #
        self.Destroy()

    def set_time(self, time):
        """sets the time in the Window name field"""
        self.SetTitle('{} - {}'.format(APP_LONG_NAME, time))

    def show_logsummary(self, logsum: Dict = None):
        txt = '{} sections, '.format(logsum['sections'])
        txt += '{} entries, '.format(logsum['entries'])
        txt += ' | '.join(['{}: {}'.format(k, v) for k, v in logsum['messages_per_level'].items()])

        self.sb.SetStatusText(txt)
        # print(self.sb)

    def clear_all(self):
        self.loglist.clear_all()
        self.settingspanel.clear_levels_emitters()
        self.sb.SetStatusText('')

    def BuildMainStructure(self):
        ################################################################
        # Define mainsplitter as child of Frame and add H and VSplitterPanel as children
        mainsplitter = wx.SplitterWindow(self, style=wx.SP_3D | wx.SP_LIVE_UPDATE)
        mainsplitter.SetMinimumPaneSize(200)
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

        self.settingspanel = SettingsPanel(splitterpanel1.BottomPanel)
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_sizer.Add(self.settingspanel, 1, wx.EXPAND)
        splitterpanel1.BottomPanel.SetSizerAndFit(bottom_sizer)


class SettingsPanel(wx.Panel):

    def __init__(self, parent=None, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.TAB_TRAVERSAL, name=''):
        super(SettingsPanel, self).__init__(parent, id=id, pos=pos, size=size, style=style, name=name)

        self.stat_1 = wx.StaticText(self, label='Show only logs from:')
        self.stat_2 = wx.StaticText(self, label='Level:')
        self.cb_emitter = wx.ComboBox(self, style=wx.CB_READONLY)
        self.cb_level = wx.ComboBox(self, choices=(), style=wx.CB_READONLY)
        self.reset_button = wx.Button(self, label='Show all')
        self.statustext = wx.StaticText(self, label='')

        base_vbox = wx.BoxSizer(wx.VERTICAL)
        self.upper = wx.WrapSizer(wx.VERTICAL)

        self.upper.Add(self.stat_1, 0, flag=wx.ALL | wx.ALIGN_CENTRE_VERTICAL, border=5)
        self.upper.Add(self.cb_emitter, 0, flag=wx.ALL | wx.ALIGN_CENTRE_VERTICAL, border=5)
        self.upper.Add(self.stat_2, 0, flag=wx.ALL | wx.ALIGN_CENTRE_VERTICAL, border=5)
        self.upper.Add(self.cb_level, 0, flag=wx.ALL | wx.ALIGN_CENTRE_VERTICAL, border=5)
        self.upper.Add(self.reset_button, 0, flag=wx.ALL | wx.ALIGN_CENTRE_VERTICAL, border=5)
        self.upper.Add(self.statustext, 0, flag=wx.ALL | wx.ALIGN_CENTRE_VERTICAL, border=5)

        base_vbox.Add(self.upper, 0)
        base_vbox.SetSizeHints(self)
        self.SetSizer(base_vbox)

        pub.subscribe(self.update_loglevels, 'logviewer.list.levels')
        pub.subscribe(self.update_emitters, 'logviewer.list.emitters')

        self.Bind(wx.EVT_COMBOBOX, self.update_list)
        self.Bind(wx.EVT_BUTTON, self.show_all, self.reset_button)

    def update_list(self, event):
        """This updates the list to show only elements with the values in the combo boxes."""
        # level is always something so we can find out at which level to show stuff
        level = self.cb_level.GetValue()
        emitter = self.cb_emitter.GetValue()
        pub.sendMessage('logviewer.list.filter', level=level, emitter=emitter)

    def show_all(self, event):
        self.cb_level.SetValue('')
        self.cb_emitter.SetValue('')
        pub.sendMessage('logviewer.list.filter', level=None, emitter=None)

    def clear_levels_emitters(self):
        self.cb_level.Clear()
        self.cb_emitter.Clear()

    def update_loglevels(self, levels: Set = None):
        self.cb_level.Clear()
        for i in levels:
            self.cb_level.Append(i)

    def update_emitters(self, emitters: Set = None):
        self.cb_emitter.Clear()
        for i in emitters:
            self.cb_emitter.Append(i)


if __name__ == '__main__':
    from LogViewer.source.main import LogViewerApp

    app = LogViewerApp()
    app.start()

    frame = MainFrame(None)
