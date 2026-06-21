import wx

class BottomRightButtons(wx.Panel):
    def __init__(self, parent ,event_manager):
        super().__init__(parent)

        self.SetBackgroundColour(parent.GetBackgroundColour())

        run_btn = wx.Button(self, label="Run")
        save_btn = wx.Button(self, label="Save")

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(run_btn, 0, wx.RIGHT, 10)
        sizer.Add(save_btn, 0)

        outer = wx.BoxSizer(wx.VERTICAL)
        outer.AddStretchSpacer()
        outer.Add(sizer, 0, wx.ALIGN_RIGHT| wx.BOTTOM, 12)  # control bottom padding here




        self.event_manager = event_manager
        run_btn.Bind(wx.EVT_BUTTON, self.on_run)
        save_btn.Bind(wx.EVT_BUTTON, self.on_save)

        self.SetSizer(outer)

    def on_run(self, event):
        self.event_manager.run_chain("run_chain")

    def on_save(self, event):
        self.event_manager.run_chain("save_chain")
        