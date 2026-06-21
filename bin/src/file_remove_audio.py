import wx
from SessionManager import (
    session_manager
)

'''
def step(context):

    frame = wx.GetTopLevelWindows()[0]

    # -------------------------------------------------
    # CHECK IF ANYTHING EXISTS
    # -------------------------------------------------
    has_loaded = (
        session_manager
        .has_loaded_audio()
    )

    has_converted = (
        session_manager
        .get_result(
            "converted_audio"
        )
        is not None
    )

    if (
        not has_loaded
        and not has_converted
    ):

        wx.MessageBox(
            "No audio to remove.",
            "Info",
            wx.OK
            | wx.ICON_INFORMATION
        )

        return "stop"

    # -------------------------------------------------
    # REMOVE OPTIONS DIALOG
    # -------------------------------------------------
    dialog = wx.SingleChoiceDialog(
        frame,
        "Choose what to remove:",
        "Remove Audio",
        [
            "Remove both",
            "Remove converted only"
        ]
    )

    dialog.SetSelection(0)

    result = dialog.ShowModal()

    if result != wx.ID_OK:
        dialog.Destroy()
        return "stop"

    choice = dialog.GetStringSelection()

    dialog.Destroy()

    # -------------------------------------------------
    # UNSAVED WORK WARNING
    # -------------------------------------------------
    if (
        session_manager
        .has_unsaved_work()
    ):

        confirm = wx.MessageBox(
            "Unsaved work will be discarded.\n\n"
            "Continue?",
            "Warning",
            (
                wx.YES_NO
                | wx.NO_DEFAULT
                | wx.ICON_WARNING
            )
        )

        if confirm != wx.YES:
            return "stop"

    # -------------------------------------------------
    # REMOVE CONVERTED ONLY
    # -------------------------------------------------
    if (
        choice
        == "Remove converted only"
    ):

        session_manager.clear_result(
            "converted_audio"
        )

    # -------------------------------------------------
    # REMOVE BOTH
    # -------------------------------------------------
    else:

        session_manager.clear_session()

    # -------------------------------------------------
    # UI UPDATE
    # -------------------------------------------------
    top = getattr(
        frame,
        "top_panel",
        None
    )

    if top:
        top.clear_audio()

    # -------------------------------------------------
    # SUCCESS
    # -------------------------------------------------
    wx.MessageBox(
        "Audio removed.",
        "Info",
        wx.OK
        | wx.ICON_INFORMATION
    )

    return "next"


'''

def step(context):

    frame = wx.GetTopLevelWindows()[0]

    # -------------------------------------------------
    # CHECK IF ANYTHING EXISTS
    # -------------------------------------------------
    has_loaded = session_manager.has_loaded_audio()
    has_converted = session_manager.get_result("converted_audio") is not None

    if not has_loaded and not has_converted:

        wx.MessageBox(
            "No audio to remove.",
            "Info",
            wx.OK | wx.ICON_INFORMATION
        )

        return "stop"

    # -------------------------------------------------
    # REMOVE OPTIONS DIALOG
    # -------------------------------------------------
    dialog = wx.SingleChoiceDialog(
        frame,
        "Choose what to remove:",
        "Remove Audio",
        ["Remove both", "Remove converted only"]
    )

    dialog.SetSelection(0)
    result = dialog.ShowModal()

    if result != wx.ID_OK:
        dialog.Destroy()
        return "stop"

    choice = dialog.GetStringSelection()
    dialog.Destroy()

    # -------------------------------------------------
    # UNSAVED WORK WARNING
    # -------------------------------------------------
    if session_manager.has_unsaved_work():

        confirm = wx.MessageBox(
            "Unsaved work will be discarded.\n\nContinue?",
            "Warning",
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING
        )

        if confirm != wx.YES:
            return "stop"

    # -------------------------------------------------
    # APPLY SESSION CHANGES
    # -------------------------------------------------
    if choice == "Remove converted only":

        session_manager.clear_result("converted_audio")

    else:

        session_manager.clear_session()

    # -------------------------------------------------
    # UI SYNC (ONLY THIS, NEVER DIRECT CLEAR)
    # -------------------------------------------------
    top = getattr(frame, "top_panel", None)

    if top:
        top.refresh_from_session()

    # -------------------------------------------------
    # SUCCESS
    # -------------------------------------------------
    wx.MessageBox(
        "Audio removed.",
        "Info",
        wx.OK | wx.ICON_INFORMATION
    )

    return "next"