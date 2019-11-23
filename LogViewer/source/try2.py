#!/usr/bin/env python2.6
# encoding: ISO-8859-1
"""
Basic Splitter Panel Skeleton.py
"""

# https://stackoverflow.com/questions/11359144/wxpython-multiple-splitter-windows

import sys

import os
import time
import wx



########################################################################

class VSplitterPanel(wx.Panel):
    """ Constructs a Vertical splitter window with left and right panels"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, color):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(color)
        splitter = wx.SplitterWindow(self, style=wx.SP_3D | wx.SP_LIVE_UPDATE)
        leftPanel = wx.Panel(splitter)
        rightPanel = wx.Panel(splitter)
        leftPanel.SetBackgroundColour('SEA GREEN')
        rightPanel.SetBackgroundColour('STEEL BLUE')

        splitter.SplitVertically(leftPanel, rightPanel)
        PanelSizer = wx.BoxSizer(wx.VERTICAL)
        PanelSizer.Add(splitter, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(PanelSizer)


########################################################################

class HSplitterPanel(wx.Panel):
    """ Constructs a Horizontal splitter window with top and bottom panels"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, color):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(color)
        splitter = wx.SplitterWindow(self, style=wx.SP_3D | wx.SP_LIVE_UPDATE)
        self.TopPanel = wx.Panel(splitter)
        self.BottomPanel = wx.Panel(splitter)
        self.TopPanel.SetBackgroundColour('YELLOW GREEN')
        self.BottomPanel.SetBackgroundColour('SLATE BLUE')

        # self.text = wx.TextCtrl(self.TopPanel, style=wx.TE_MULTILINE)
        # top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # top_sizer.Add(self.text, 1, wx.EXPAND)
        # self.TopPanel.SetSizerAndFit(top_sizer)



        splitter.SplitHorizontally(self.TopPanel, self.BottomPanel)
        self.PanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.PanelSizer.Add(splitter, 1, wx.EXPAND | wx.ALL)

        self.SetSizer(self.PanelSizer)


########################################################################

class MainFrame(wx.Frame):
    """Constructor"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, id):
        wx.Frame.__init__(self, None, title="Basic Splitter Panel Skeleton", size=(800, 600))
        self.sb = self.CreateStatusBar()
        ################################################################
        # Define mainsplitter as child of Frame and add H and VSplitterPanel as children
        mainsplitter = wx.SplitterWindow(self, style=wx.SP_3D | wx.SP_LIVE_UPDATE)
        splitterpanel1 = HSplitterPanel(mainsplitter, 'LIGHT BLUE')

        right_panel = wx.Panel(mainsplitter)

        mainsplitter.SplitVertically(splitterpanel1, right_panel)
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        MainSizer.Add(mainsplitter, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(MainSizer)

        self.text = wx.TextCtrl(splitterpanel1.TopPanel, style=wx.TE_MULTILINE)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(self.text, 1, wx.EXPAND)
        splitterpanel1.TopPanel.SetSizerAndFit(top_sizer)

        languages = ['C', 'C++', 'Java', 'Python', 'Perl', 'JavaScript', 'PHP', 'VB.NET', 'C#']
        self.lst = wx.ListBox(splitterpanel1.BottomPanel, size=(100, 300), choices=languages, style=wx.LB_SINGLE)
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_sizer.Add(self.lst, 1, wx.EXPAND)
        splitterpanel1.BottomPanel.SetSizerAndFit(bottom_sizer)

        self.text2 = wx.TextCtrl(right_panel, style=wx.TE_MULTILINE)
        right_sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_sizer.Add(self.text2, 1, wx.EXPAND)
        right_panel.SetSizerAndFit(right_sizer)

        self.Bind(wx.EVT_LISTBOX, self.onListBox, self.lst)


        #################################################################
        self.Show()

    def onListBox(self, event):
        self.text.AppendText( "Current selection: " + event.GetEventObject().GetStringSelection() +"\n")
        self.text2.AppendText( "Current selection: " + event.GetEventObject().GetStringSelection() +"\n")


# ----------------------------------------------------------------------


if __name__ == '__main__':
    app = wx.App()
    MainFrame(None, -1)
    app.MainLoop()
