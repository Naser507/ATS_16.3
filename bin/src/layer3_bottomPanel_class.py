import wx

class BottomPanelBase(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.SetMinSize((-1, 150))

        self.SetMinSize((-1, 150))

        # OS-like border
        self.SetWindowStyle(wx.BORDER_THEME)

        # Scrollable area
        self.scroll = wx.ScrolledWindow(self)
        self.scroll.SetScrollRate(5, 5)

        # Inner content sizer with padding
        self.inner_sizer = wx.BoxSizer(wx.VERTICAL)

        wrapper = wx.BoxSizer(wx.VERTICAL)
        wrapper.Add(self.inner_sizer, 1, wx.EXPAND | wx.ALL, 10)

        self.scroll.SetSizer(wrapper)

        # Layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.scroll, 1, wx.EXPAND)

        self.SetSizer(main_sizer)

        self.SetBackgroundColour(wx.Colour(220, 220, 220))  # placeholder background color