import wx

def step(context):
    wx.MessageBox("You clicked the Run button !!", "Info", wx.OK | wx.ICON_INFORMATION)
    return "stop"