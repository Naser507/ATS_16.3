import wx
from dynamicLoader import loader

def main():
    app = wx.App(False)
    # Load the main frame module from src via dynamicLoader
    frame_module = loader.load("appMainFrame")
    if frame_module:
        frame = frame_module.MainFrame(None, title="ATS 16.1")
        frame.Show()
        app.MainLoop()

if __name__ == "__main__":
    main()