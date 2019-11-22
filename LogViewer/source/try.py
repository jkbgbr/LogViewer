import wx


class Mywin(wx.Frame):

    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(350, 300))

        languages = ['C', 'C++', 'Java', 'Python', 'Perl',
                     'JavaScript', 'PHP', 'VB.NET', 'C#']

        splitter = wx.SplitterWindow(self, -1)

        panel1 = wx.Panel(splitter, -1)
        b = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.TextCtrl(panel1, style=wx.TE_MULTILINE)
        b.Add(self.text, 1, wx.EXPAND)
        panel1.SetSizerAndFit(b)

        panel2 = wx.Panel(splitter, -1)
        lst = wx.ListBox(panel2, size=(100, 300), choices=languages, style=wx.LB_SINGLE)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(lst, 1)
        panel2.SetSizer(hbox1)

        splitter.SplitHorizontally(panel2, panel1)
        self.Centre()
        self.Show(True)


ex = wx.App()
Mywin(None, 'Splitter Demo')
ex.MainLoop()