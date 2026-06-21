import wx
from EventManager import event_manager


class FileMenu:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

        # Create File menu
        self.menu = wx.Menu()

        # Menu items
        self.new_audio = self.menu.Append(
            wx.ID_ANY,
            "New Audio"
        )

        self.remove_audio = self.menu.Append(
            wx.ID_ANY,
            "Remove Audio"
        )

        self.convert_audio = self.menu.Append(
            wx.ID_ANY,
            "Convert Audio"
        )

        self.save_converted = self.menu.Append(
            wx.ID_ANY,
            "Save Converted"
        )

        # Separator
        self.menu.AppendSeparator()

        self.exit_item = self.menu.Append(
            wx.ID_ANY,
            "Exit"
        )

        # Bind events
        parent_frame.Bind(
            wx.EVT_MENU,
            self.on_new_audio,
            self.new_audio
        )

        parent_frame.Bind(
            wx.EVT_MENU,
            self.on_remove_audio,
            self.remove_audio
        )

        parent_frame.Bind(
            wx.EVT_MENU,
            self.on_convert_audio,
            self.convert_audio
        )

        parent_frame.Bind(
            wx.EVT_MENU,
            self.on_save_converted,
            self.save_converted
        )

        parent_frame.Bind(
            wx.EVT_MENU,
            self.on_exit,
            self.exit_item
        )

    # -----------------------------
    # Event handlers
    # -----------------------------
    def on_new_audio(self, event):
        event_manager.run_chain("file_new_audio")

    def on_remove_audio(self, event):
        event_manager.run_chain("file_remove_audio")

    def on_convert_audio(self, event):
        event_manager.run_chain("file_convert_audio")

    def on_save_converted(self, event):
        event_manager.run_chain("file_save_audio")

    def on_exit(self, event):
        event_manager.run_chain("app_exit")