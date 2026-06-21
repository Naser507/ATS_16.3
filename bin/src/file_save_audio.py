import wx
import os
import json
import shutil
from SessionManager import session_manager


CONFIG_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "config"
)

CACHE_FILE = os.path.join(
    CONFIG_FOLDER,
    "last_save_path.json"
)


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


def save_last_path(path):
    os.makedirs(CONFIG_FOLDER, exist_ok=True)

    with open(CACHE_FILE, "w") as f:
        json.dump({"last_path": path}, f, indent=4)



'''
def step(context):
    frame = wx.GetTopLevelWindows()[0]
    top = getattr(frame, "top_panel", None)

    if not top:
        return "stop"

    # -----------------------------
    # Get converted audio
    # -----------------------------
    input_path = context.data.get("converted_audio_path")

    if not input_path:
        wx.MessageBox(
            "No converted audio to save.",
            "Error",
            wx.OK | wx.ICON_ERROR
        )
        return "stop"

    initial_dir = load_last_path()

    # -----------------------------
    # Save dialog
    # -----------------------------
    with wx.FileDialog(
        frame,
        "Save Converted Audio",
        defaultDir=initial_dir,
        wildcard="WAV files (*.wav)|*.wav",
        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
    ) as dialog:

        if dialog.ShowModal() == wx.ID_CANCEL:
            return "stop"

        output_path = dialog.GetPath()

    # Ensure .wav extension
    if not output_path.lower().endswith(".wav"):
        output_path += ".wav"

    # -----------------------------
    # Copy file (for now)
    # -----------------------------
    try:
        shutil.copyfile(input_path, output_path)

    except Exception as e:
        wx.MessageBox(
            f"Save failed:\n{str(e)}",
            "Error",
            wx.OK | wx.ICON_ERROR
        )
        return "stop"

    # -----------------------------
    # Update context
    # -----------------------------
    context.data["is_saved"] = True

    if hasattr(top, "context"):
        top.context["is_saved"] = True

    # -----------------------------
    # Cache path
    # -----------------------------
    save_last_path(os.path.dirname(output_path))

    wx.MessageBox(
        "Audio saved successfully!",
        "Success",
        wx.OK | wx.ICON_INFORMATION
    )

    return "next"

'''


'''
def step(context):

    frame = wx.GetTopLevelWindows()[0]

    # -------------------------------------------------
    # CHECK IF ANY GENERATED AUDIO EXISTS
    # -------------------------------------------------
    output_path = session_manager.get_generated_audio()

    if not output_path:
        wx.MessageBox(
            "No converted audio to save.",
            "Info",
            wx.OK | wx.ICON_INFORMATION
        )
        return "stop"

    # -------------------------------------------------
    # (FUTURE EXTENSION POINT)
    # Here we can later open Save File Dialog
    # -------------------------------------------------
    # For now: we assume conversion output is "saved"

    # -------------------------------------------------
    # SESSION UPDATE
    # -------------------------------------------------
    session_manager.mark_saved()

    # -------------------------------------------------
    # SUCCESS MESSAGE
    # -------------------------------------------------
    wx.MessageBox(
        "Audio marked as saved.",
        "Success",
        wx.OK | wx.ICON_INFORMATION
    )

    return "next"


'''
def step(context):

    frame = wx.GetTopLevelWindows()[0]

    # -------------------------------------------------
    # GET CONVERTED AUDIO
    # -------------------------------------------------
    input_path = (
        session_manager.get_result(
            "converted_audio"
        )
    )

    if not input_path:

        wx.MessageBox(
            "No converted audio to save.",
            "Info",
            wx.OK
            | wx.ICON_INFORMATION
        )

        return "stop"

    # -------------------------------------------------
    # LAST SAVE FOLDER
    # -------------------------------------------------
    initial_dir = (
        session_manager
        .get_last_save_folder()
    )

    if not initial_dir:
        initial_dir = os.path.expanduser(
            "~"
        )

    # -------------------------------------------------
    # DEFAULT FILE NAME
    # -------------------------------------------------
    default_name = os.path.basename(
        input_path
    )

    # -------------------------------------------------
    # SAVE DIALOG
    # -------------------------------------------------
    with wx.FileDialog(
        frame,
        "Save Converted Audio",
        defaultDir=initial_dir,
        defaultFile=default_name,
        wildcard=(
            "WAV files (*.wav)|*.wav"
        ),
        style=(
            wx.FD_SAVE
            | wx.FD_OVERWRITE_PROMPT
        )
    ) as dialog:

        if (
            dialog.ShowModal()
            == wx.ID_CANCEL
        ):
            return "stop"

        output_path = (
            dialog.GetPath()
        )

    # -------------------------------------------------
    # ENSURE EXTENSION
    # -------------------------------------------------
    if not (
        output_path
        .lower()
        .endswith(".wav")
    ):

        output_path += ".wav"

    # -------------------------------------------------
    # COPY FILE
    # -------------------------------------------------
    try:

        shutil.copyfile(
            input_path,
            output_path
        )

    except Exception as e:

        wx.MessageBox(
            (
                "Save failed:\n"
                + str(e)
            ),
            "Error",
            wx.OK
            | wx.ICON_ERROR
        )

        return "stop"

    # -------------------------------------------------
    # UPDATE CACHE
    # -------------------------------------------------
    session_manager.set_last_save_folder(
        os.path.dirname(
            output_path
        )
    )

    # -------------------------------------------------
    # MARK SAVED
    # -------------------------------------------------
    session_manager.mark_saved(
        "converted_audio"
    )

    # -------------------------------------------------
    # SUCCESS
    # -------------------------------------------------
    wx.MessageBox(
        "Audio saved successfully!",
        "Success",
        wx.OK
        | wx.ICON_INFORMATION
    )

    return "next"