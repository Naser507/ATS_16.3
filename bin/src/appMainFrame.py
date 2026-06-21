import wx
from dynamicLoader import loader
from EventManager import event_manager
from SessionManager import session_manager


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(
            parent,
            title=title,
            size=(800, 600)
        )

        # ---------------------------------
        # Close event
        # ---------------------------------
        self.Bind(
            wx.EVT_CLOSE,
            self.on_close
        )

        # ---------------------------------
        # Temporary background
        # ---------------------------------
        self.SetBackgroundColour(
            wx.Colour(200, 200, 200)
        )

        # ---------------------------------
        # Root container
        # ---------------------------------
        self.container = wx.Panel(self)

        self.container.SetBackgroundColour(
            self.GetBackgroundColour()
        )

        # ---------------------------------
        # Load modules dynamically
        # ---------------------------------
        menu_module = loader.load(
            "layer1_menuStrip"
        )

        top_panel_module = loader.load(
            "topPanel"
        )

        bottom_empty_module = loader.load(
            "bottomPanelEmpty"
        )

        buttons_module = loader.load(
            "layer4_bottomRightButtons"
        )

        # ---------------------------------
        # Menu bar
        # ---------------------------------
        if menu_module:
            menu_bar = menu_module.MenuStrip(self)
            self.SetMenuBar(menu_bar)

        # ---------------------------------
        # Create UI components
        # ---------------------------------
        top_panel = (
            top_panel_module.TopPanel(self.container)
            if top_panel_module
            else None
        )

        bottom_panel = (
            bottom_empty_module.BottomPanel(
                self.container
            )
            if bottom_empty_module
            else None
        )

        buttons_panel = (
            buttons_module.BottomRightButtons(
                self.container,
                event_manager
            )
            if buttons_module
            else None
        )

        # ---------------------------------
        # Save references
        # ---------------------------------
        self.top_panel = top_panel
        self.bottom_panel = bottom_panel
        self.buttons_panel = buttons_panel

        # ---------------------------------
        # Layout
        # ---------------------------------
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        if top_panel:
            main_sizer.Add(
                top_panel,
                0,
                wx.EXPAND | wx.BOTTOM,
                10
            )

        if bottom_panel:
            main_sizer.Add(
                bottom_panel,
                1,
                wx.EXPAND | wx.BOTTOM,
                10
            )

        if buttons_panel:
            main_sizer.Add(
                buttons_panel,
                0,
                wx.EXPAND
            )

        # ---------------------------------
        # Global frame padding
        # ---------------------------------
        wrapper = wx.BoxSizer(wx.VERTICAL)

        wrapper.Add(
            main_sizer,
            1,
            wx.EXPAND | wx.ALL,
            10
        )

        self.container.SetSizer(wrapper)

        self.Centre()

    # =================================================
    # CLOSE HANDLER
    # =================================================
    def on_close(self, event):

        # ---------------------------------------------
        # CHECK UNSAVED WORK
        # ---------------------------------------------
        if session_manager.has_unsaved_work():

            choice = wx.MessageBox(
                "You have unsaved converted audio.\n\n"
                "Do you want to exit anyway?",
                "Exit Warning",
                wx.YES_NO | wx.CANCEL | wx.ICON_WARNING
            )

            if choice == wx.NO or choice == wx.CANCEL:
                event.Veto()
                return

        # ---------------------------------------------
        # CLEAN EXIT
        # ---------------------------------------------
        self.Destroy()