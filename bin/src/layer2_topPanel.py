import wx


class TopPanelBase(wx.Panel):
    def __init__(self, parent):
        super().__init__(
            parent,
            size=(-1, 120)
        )

        # -----------------------------
        # Minimum size
        # -----------------------------
        self.SetMinSize((-1, 80))

        # -----------------------------
        # OS-style border
        # -----------------------------
        self.SetWindowStyle(
            wx.BORDER_THEME
        )

        # -----------------------------
        # Scrollable area
        # -----------------------------
        self.scroll = wx.ScrolledWindow(
            self
        )

        self.scroll.SetScrollRate(5, 5)

        # -----------------------------
        # Inner content sizer
        # (actual widgets go here)
        # -----------------------------
        self.content_sizer = wx.BoxSizer(
            wx.VERTICAL
        )

        # -----------------------------
        # Wrapper padding
        # -----------------------------
        wrapper = wx.BoxSizer(wx.VERTICAL)

        wrapper.Add(
            self.content_sizer,
            1,
            wx.EXPAND | wx.ALL,
            10
        )

        self.scroll.SetSizer(wrapper)

        # -----------------------------
        # Main layout
        # -----------------------------
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(
            self.scroll,
            1,
            wx.EXPAND
        )

        self.SetSizer(main_sizer)

        # Temporary placeholder color
        self.SetBackgroundColour(
            wx.Colour(220, 220, 220)
        )