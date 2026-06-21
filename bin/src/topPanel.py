import wx
from SessionManager import session_manager


class TopPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent, size=(-1, 120))

        # -------------------------------------------------
        # VISUAL SETUP (UNCHANGED)
        # -------------------------------------------------
        self.SetMinSize((-1, 120 - 30))
        self.SetBackgroundColour(wx.Colour(220, 220, 220))
        self.SetWindowStyle(wx.BORDER_THEME)

        # -------------------------------------------------
        # LAYOUT (UNCHANGED)
        # -------------------------------------------------
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        grid = wx.FlexGridSizer(2, 2, 10, 10)
        grid.AddGrowableCol(1, 1)

        # -----------------------------
        # Loaded audio row
        # -----------------------------
        grid.Add(
            wx.StaticText(self, label="Loaded Audio:"),
            0,
            wx.ALIGN_CENTER_VERTICAL
        )

        self.loaded_audio_box = wx.TextCtrl(
            self,
            style=wx.TE_READONLY
        )

        grid.Add(self.loaded_audio_box, 1, wx.EXPAND)

        # -----------------------------
        # Converted audio row
        # -----------------------------
        grid.Add(
            wx.StaticText(self, label="Converted Audio:"),
            0,
            wx.ALIGN_CENTER_VERTICAL
        )

        self.converted_audio_box = wx.TextCtrl(
            self,
            style=wx.TE_READONLY
        )

        grid.Add(self.converted_audio_box, 1, wx.EXPAND)

        main_sizer.Add(grid, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(main_sizer)

        # -------------------------------------------------
        # INITIAL SYNC
        # -------------------------------------------------
        self.refresh_from_session()

    # =================================================
    # CORE METHOD (NEW SINGLE SOURCE OF TRUTH)
    # =================================================
    def refresh_from_session(self):

        # -----------------------------
        # Loaded audio
        # -----------------------------
        loaded = session_manager.get_loaded_audio()

        if loaded:
            self.loaded_audio_box.SetValue(loaded)
        else:
            self.loaded_audio_box.SetValue("")

        # -----------------------------
        # Converted audio
        # -----------------------------
        converted = session_manager.get_result("converted_audio")

        if converted:
            self.converted_audio_box.SetValue(converted)
        else:
            self.converted_audio_box.SetValue("")

    # =================================================
    # OPTIONAL: manual setters removed conceptually
    # (kept only for backward safety if needed)
    # =================================================

    '''
    def set_loaded_audio(self, path):
        # now just sync session view (not direct truth)
        self.refresh_from_session()

    def set_converted_audio(self, path):
        self.refresh_from_session()
    '''

    def set_loaded_audio(self, path=None):
        self.refresh_from_session()

    def set_converted_audio(self, path=None):
        self.refresh_from_session()


    def clear_audio(self):
        # NEVER directly clears UI anymore
        #session_manager.clear_session()
        self.refresh_from_session()