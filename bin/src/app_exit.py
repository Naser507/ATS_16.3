import wx
from SessionManager import session_manager


def step(context):

    frame = wx.GetTopLevelWindows()[0]

    # -------------------------------------------------
    # UNSAVED WORK CHECK
    # -------------------------------------------------
    if session_manager.has_unsaved_work():

        choice = wx.MessageBox(
            "You have unsaved converted audio.\n\n"
            "Exit anyway and discard it?",
            "Confirm Exit",
            wx.YES_NO | wx.CANCEL | wx.ICON_WARNING
        )

        if choice != wx.YES:
            return "stop"

        # user confirmed discard
        session_manager.clear_session()

    # -------------------------------------------------
    # CLEAN EXIT
    # -------------------------------------------------
    app = wx.GetApp()

    if app:
        app.ExitMainLoop()

    return "stop"