
'''
import wx

def create_menu(frame):
    menubar = wx.MenuBar()

    file_menu = wx.Menu()
    view_menu = wx.Menu()
    dsp_menu = wx.Menu()
    conversion_menu = wx.Menu()
    about_menu = wx.Menu()

    menubar.Append(file_menu, "File")
    menubar.Append(view_menu, "View")
    menubar.Append(dsp_menu, "DSP")
    menubar.Append(conversion_menu, "Conversion")
    menubar.Append(about_menu, "About")

    frame.SetMenuBar(menubar)

'''

import wx
from dynamicLoader import loader


class MenuStrip(wx.MenuBar):
    def __init__(self, parent_frame):
        super().__init__()

        # -----------------------------
        # Load File Menu dynamically
        # -----------------------------
        file_menu_module = loader.load("menu_file")

        if file_menu_module:
            file_menu = file_menu_module.FileMenu(parent_frame)

            self.Append(
                file_menu.menu,
                "File"
            )

        # -----------------------------
        # Placeholder menus
        # -----------------------------
        self.Append(wx.Menu(), "View")
        self.Append(wx.Menu(), "DSP")
        self.Append(wx.Menu(), "Conversion")
        self.Append(wx.Menu(), "About")