import wx
import os
import json
from SessionManager import session_manager



CONFIG_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "config"
)

CACHE_FILE = os.path.join(
    CONFIG_FOLDER,
    "last_audio_path.json"
)


# -------------------------------------------------
# Load cached folder
# -------------------------------------------------
def load_last_path():
    default_path = os.path.expanduser("~")

    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                data = json.load(f)

            path = data.get("last_path")

            if path and os.path.exists(path):
                return path

    except Exception:
        try:
            os.remove(CACHE_FILE)
        except Exception:
            pass

    return default_path


# -------------------------------------------------
# Save cached folder
# -------------------------------------------------
def save_last_path(path):
    os.makedirs(
        CONFIG_FOLDER,
        exist_ok=True
    )

    with open(CACHE_FILE, "w") as f:
        json.dump(
            {"last_path": path},
            f,
            indent=4
        )


# -------------------------------------------------
# Event Step
# -------------------------------------------------

'''
def step(context):

    frame = wx.GetTopLevelWindows()[0]

    # ---------------------------------------------
    # File dialog
    # ---------------------------------------------
    initial_dir = load_last_path()

    with wx.FileDialog(
        frame,
        "Select Audio File",
        defaultDir=initial_dir,
        wildcard=(
            "Audio Files (*.mp3;*.wav)|"
            "*.mp3;*.wav"
        ),
        style=wx.FD_OPEN |
        wx.FD_FILE_MUST_EXIST
    ) as dialog:

        if dialog.ShowModal() == wx.ID_CANCEL:
            return "stop"

        selected_path = dialog.GetPath()

    # ---------------------------------------------
    # Validate extension
    # ---------------------------------------------
    extension = os.path.splitext(
        selected_path
    )[1].lower()

    match extension:

        case ".mp3":
            pass

        case ".wav":
            pass

        case _:
            wx.MessageBox(
                "Unsupported audio format.",
                "Error",
                wx.OK | wx.ICON_ERROR
            )
            return "stop"

    # ---------------------------------------------
    # Save last folder
    # ---------------------------------------------
    save_last_path(
        os.path.dirname(
            selected_path
        )
    )

    # ---------------------------------------------
    # Update EVENT CONTEXT
    # (source of truth)
    # ---------------------------------------------
    context.data[
        "loaded_audio_path"
    ] = selected_path

    context.data[
        "generated_audio_path"
    ] = None

    context.data[
        "save_state"
    ] = "undecided"

    # ---------------------------------------------
    # Future memory pipeline placeholder
    # ---------------------------------------------
    context.data[
        "memory_audio"
    ] = None

    # ---------------------------------------------
    # Update top panel UI
    # ---------------------------------------------
    if hasattr(frame, "top_panel"):
        frame.top_panel.set_loaded_audio(
            selected_path
        )

    return "next"

'''
'''
def step(context):

    frame = wx.GetTopLevelWindows()[0]

    # -------------------------------------------------
    # File dialog
    # -------------------------------------------------
    with wx.FileDialog(
        frame,
        "Select Audio File",
        wildcard="Audio Files (*.mp3;*.wav)|*.mp3;*.wav",
        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    ) as dialog:

        if dialog.ShowModal() == wx.ID_CANCEL:
            return "stop"

        selected_path = dialog.GetPath()

    # -------------------------------------------------
    # Validate format
    # -------------------------------------------------
    ext = os.path.splitext(selected_path)[1].lower()

    if ext not in [".mp3", ".wav"]:
        wx.MessageBox(
            "Unsupported audio format.",
            "Error",
            wx.OK | wx.ICON_ERROR
        )
        return "stop"

    # -------------------------------------------------
    # SESSION UPDATE (NEW CORE ADDITION)
    # -------------------------------------------------
    session_manager.set_loaded_audio(selected_path)

    # -------------------------------------------------
    # UI UPDATE (existing behavior)
    # -------------------------------------------------
    if hasattr(frame, "top_panel"):
        frame.top_panel.set_loaded_audio(selected_path)

    return "next"

'''

'''
def step(context):

    frame = wx.GetTopLevelWindows()[0]

    # -------------------------------------------------
    # ACTIVE SESSION CHECK
    # Prevent silent replacement
    # -------------------------------------------------
    if session_manager.has_loaded_audio():

        if session_manager.is_transient():

            choice = wx.MessageBox(
                "You have unsaved work.\n\n"
                "Would you like to continue?\n"
                "Unsaved results may be lost.",
                "Replace Current Audio?",
                wx.YES_NO | wx.CANCEL | wx.ICON_WARNING
            )

            # CANCEL
            if choice == wx.CANCEL:
                return "stop"

            # NO
            if choice == wx.NO:
                return "stop"

            # YES
            # discard current temporary work
            session_manager.clear_session()

        else:

            choice = wx.MessageBox(
                "Another audio file is already loaded.\n\n"
                "Replace it?",
                "Replace Audio?",
                wx.YES_NO | wx.CANCEL | wx.ICON_WARNING
            )

            if choice != wx.YES:
                return "stop"

            session_manager.clear_session()

    # -------------------------------------------------
    # Get cached folder from SessionManager
    # -------------------------------------------------
    initial_dir = (
        session_manager
        .get_last_open_folder()
    )

    if not initial_dir:
        initial_dir = os.path.expanduser("~")

    # -------------------------------------------------
    # File dialog
    # -------------------------------------------------
    with wx.FileDialog(
        frame,
        "Select Audio File",
        defaultDir=initial_dir,
        wildcard=(
            "Audio Files (*.mp3;*.wav)|"
            "*.mp3;*.wav"
        ),
        style=(
            wx.FD_OPEN
            | wx.FD_FILE_MUST_EXIST
        )
    ) as dialog:

        if dialog.ShowModal() == wx.ID_CANCEL:
            return "stop"

        selected_path = dialog.GetPath()

    # -------------------------------------------------
    # Validate format
    # -------------------------------------------------
    ext = os.path.splitext(
        selected_path
    )[1].lower()

    if ext not in [
        ".mp3",
        ".wav"
    ]:

        wx.MessageBox(
            "Unsupported audio format.",
            "Error",
            wx.OK | wx.ICON_ERROR
        )

        return "stop"

    # -------------------------------------------------
    # SessionManager update
    # -------------------------------------------------
    session_manager.set_loaded_audio(
        selected_path
    )

    # -------------------------------------------------
    # Save last open folder
    # (SessionManager owns cache now)
    # -------------------------------------------------
    session_manager.set_last_open_folder(
        os.path.dirname(
            selected_path
        )
    )

    # -------------------------------------------------
    # UI update
    # -------------------------------------------------
    if hasattr(
        frame,
        "top_panel"
    ):

        frame.top_panel.set_loaded_audio(
            selected_path
        )

    return "next"


'''

'''
def step(context):

    frame = wx.GetTopLevelWindows()[0]

    # -------------------------------------------------
    # If audio already loaded → warn first
    # -------------------------------------------------
    if session_manager.get_loaded_audio():

        choice = wx.MessageBox(
            "Audio already loaded.\n\n"
            "Do you want to replace it?",
            "Warning",
            wx.YES_NO | wx.ICON_WARNING
        )

        if choice != wx.YES:
            return "stop"

    # -------------------------------------------------
    # FILE DIALOG (ONLY AFTER CONFIRMATION)
    # -------------------------------------------------
    with wx.FileDialog(
        frame,
        "Select Audio File",
        wildcard="Audio Files (*.mp3;*.wav)|*.mp3;*.wav",
        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    ) as dialog:

        if dialog.ShowModal() != wx.ID_OK:
            return "stop"

        selected_path = dialog.GetPath()

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------
    ext = os.path.splitext(selected_path)[1].lower()

    if ext not in [".mp3", ".wav"]:

        wx.MessageBox(
            "Unsupported audio format.",
            "Error",
            wx.OK | wx.ICON_ERROR
        )

        return "stop"

    # -------------------------------------------------
    # SESSION UPDATE (ONLY HERE)
    # -------------------------------------------------
    session_manager.set_loaded_audio(selected_path)

    # IMPORTANT: reset dependent state
    session_manager.clear_result("converted_audio")

    # -------------------------------------------------
    # UI SYNC (single source of truth)
    # -------------------------------------------------
    top = getattr(frame, "top_panel", None)

    if top:
        top.refresh_from_session()

    return "next"



'''

def step(context):

    frame = wx.GetTopLevelWindows()[0]

    # -------------------------------------------------
    # If audio already loaded → warn first
    # -------------------------------------------------
    if session_manager.get_loaded_audio():

        choice = wx.MessageBox(
            "Audio already loaded.\n\n"
            "Do you want to replace it?",
            "Warning",
            wx.YES_NO | wx.ICON_WARNING
        )

        if choice != wx.YES:
            return "stop"

    # -------------------------------------------------
    # FILE DIALOG
    # -------------------------------------------------
    with wx.FileDialog(
        frame,
        "Select Audio File",
        wildcard="Audio Files (*.mp3;*.wav)|*.mp3;*.wav",
        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    ) as dialog:

        if dialog.ShowModal() != wx.ID_OK:
            return "stop"

        selected_path = dialog.GetPath()

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------
    ext = os.path.splitext(selected_path)[1].lower()

    if ext not in [".mp3", ".wav"]:

        wx.MessageBox(
            "Unsupported audio format.",
            "Error",
            wx.OK | wx.ICON_ERROR
        )

        return "stop"

    # -------------------------------------------------
    # SESSION UPDATE
    # -------------------------------------------------
    session_manager.set_loaded_audio(selected_path)

    session_manager.clear_result("converted_audio")

    # -------------------------------------------------
    # UI SYNC (IMPORTANT FIX)
    # -------------------------------------------------
    top = getattr(frame, "top_panel", None)

    if top:
        top.refresh_from_session()

    return "next"