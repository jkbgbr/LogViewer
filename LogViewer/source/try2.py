#!/usr/bin/env python2.6
# encoding: ISO-8859-1
"""
Basic Splitter Panel Skeleton.py
"""

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
        # splitterpanel1 = HSplitterPanel(mainsplitter,'LIGHT BLUE')
        splitterpanel1 = HSplitterPanel(mainsplitter, 'LIGHT BLUE')
        # splitterpanel2 = VSplitterPanel(mainsplitter,'LIGHT BLUE')

        # print self.GetChildren(),'\n'
        # print splitterpanel1.leftPanel.GetChildren()
        mainsplitter.SplitVertically(splitterpanel1, wx.Panel(mainsplitter))
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        MainSizer.Add(mainsplitter, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(MainSizer)

        self.text = wx.TextCtrl(splitterpanel1.TopPanel, style=wx.TE_MULTILINE)
        splitterpanel1.PanelSizer.Add(self.text, 1, wx.EXPAND)
        # splitterpanel1.TopPanel.SetSizerAndFit(splitterpanel1.PanelSizer)

        # languages = ['C', 'C++', 'Java', 'Python', 'Perl',
        #              'JavaScript', 'PHP', 'VB.NET', 'C#']
        # lst = wx.ListBox(splitterpanel1.BottomPanel, size=(100, 300), choices=languages, style=wx.LB_SINGLE)


        #################################################################
        self.Show()


# ----------------------------------------------------------------------


if __name__ == '__main__':
    app = wx.App()
    MainFrame(None, -1)
    app.MainLoop()
