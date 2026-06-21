from SessionManager import session_manager
import wx
import os
import shutil
import subprocess



from audio_temp_manager import (
    get_temp_results_folder,
    get_safe_output_path
)

'''
def step(context):

    # -------------------------------------------------
    # Get currently loaded audio
    # -------------------------------------------------
    input_path = context.data.get(
        "loaded_audio_path"
    )

    if not input_path:
        wx.MessageBox(
            "No audio loaded.",
            "Error",
            wx.OK | wx.ICON_ERROR
        )
        return "stop"

    # -------------------------------------------------
    # Determine file extension
    # -------------------------------------------------
    extension = os.path.splitext(
        input_path
    )[1].lower()

    # -------------------------------------------------
    # Create temp results folder
    # automatically if missing
    # -------------------------------------------------
    temp_folder = (
        get_temp_results_folder()
    )

    # -------------------------------------------------
    # Create output filename
    # Example:
    # song.mp3 → song.wav
    # -------------------------------------------------
    input_name = os.path.basename(
        input_path
    )

    output_name = (
        os.path.splitext(
            input_name
        )[0] + ".wav"
    )

    output_path = (
        get_safe_output_path(
            temp_folder,
            output_name
        )
    )

    # =================================================
    # WAV FILE
    # Just copy into temp folder
    # =================================================
    if extension == ".wav":

        try:
            shutil.copy2(
                input_path,
                output_path
            )

        except Exception as e:
            wx.MessageBox(
                f"Copy failed:\n{str(e)}",
                "Error",
                wx.OK | wx.ICON_ERROR
            )
            return "stop"

    # =================================================
    # MP3 FILE
    # Use converter binary
    # =================================================
    elif extension == ".mp3":

        root = os.path.dirname(
            os.path.dirname(__file__)
        )

        converter_binary = os.path.join(
            root,
            "audio_converter"
        )

        try:
            result = subprocess.run(
                [
                    converter_binary,
                    input_path,
                    output_path
                ],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                wx.MessageBox(
                    (
                        "Conversion failed:\n"
                        + result.stderr
                    ),
                    "Error",
                    wx.OK |
                    wx.ICON_ERROR
                )
                return "stop"

        except Exception as e:
            wx.MessageBox(
                (
                    "Failed to launch "
                    "converter:\n"
                    + str(e)
                ),
                "Error",
                wx.OK |
                wx.ICON_ERROR
            )
            return "stop"

    # =================================================
    # Unsupported file
    # =================================================
    else:
        wx.MessageBox(
            "Unsupported format.",
            "Error",
            wx.OK |
            wx.ICON_ERROR
        )
        return "stop"

    # -------------------------------------------------
    # Update context
    # -------------------------------------------------
    context.data[
        "generated_audio_path"
    ] = output_path

    context.data[
        "save_state"
    ] = "undecided"

    # -------------------------------------------------
    # Update top panel UI
    # -------------------------------------------------
    frame = wx.GetTopLevelWindows()[0]

    if hasattr(frame, "top_panel"):
        frame.top_panel.set_converted_audio(
            output_path
        )

    # -------------------------------------------------
    # Success message
    # -------------------------------------------------
    wx.MessageBox(
        "Audio converted successfully!",
        "Success",
        wx.OK |
        wx.ICON_INFORMATION
    )

    return "next"

'''

'''

def step(context):

    frame = wx.GetTopLevelWindows()[0]

    # -------------------------------------------------
    # GET LOADED AUDIO (SESSION SOURCE OF TRUTH)
    # -------------------------------------------------
    input_path = session_manager.get_loaded_audio()

    if not input_path:
        wx.MessageBox(
            "No audio loaded.",
            "Error",
            wx.OK | wx.ICON_ERROR
        )
        return "stop"

    # -------------------------------------------------
    # UNSAVED WORK PROTECTION
    # -------------------------------------------------
    if session_manager.has_unsaved_work():
        choice = wx.MessageBox(
            "Unsaved converted audio exists.\n\n"
            "Do you want to continue and overwrite it?",
            "Warning",
            wx.YES_NO | wx.CANCEL | wx.ICON_WARNING
        )

        if choice == wx.NO:
            session_manager.mark_discarded()
        elif choice == wx.CANCEL:
            return "stop"

    # -------------------------------------------------
    # FILE TYPE CHECK
    # -------------------------------------------------
    ext = os.path.splitext(input_path)[1].lower()

    # -------------------------------------------------
    # OUTPUT PATH
    # -------------------------------------------------
    root = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(
        root,
        "temp_output.wav"
    )

    # =================================================
    # WAV → COPY
    # =================================================
    if ext == ".wav":

        try:
            shutil.copy2(input_path, output_path)

        except Exception as e:
            wx.MessageBox(
                f"Copy failed:\n{str(e)}",
                "Error",
                wx.OK | wx.ICON_ERROR
            )
            return "stop"

    # =================================================
    # MP3 → CALL C++ BINARY
    # =================================================
    elif ext == ".mp3":

        binary_path = os.path.join(
            root,
            "audio_converter"
        )

        try:
            result = subprocess.run(
                [binary_path, input_path, output_path],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                wx.MessageBox(
                    "Conversion failed:\n" + result.stderr,
                    "Error",
                    wx.OK | wx.ICON_ERROR
                )
                return "stop"

        except Exception as e:
            wx.MessageBox(
                "Failed to run converter:\n" + str(e),
                "Error",
                wx.OK | wx.ICON_ERROR
            )
            return "stop"

    else:
        wx.MessageBox(
            "Unsupported format.",
            "Error",
            wx.OK | wx.ICON_ERROR
        )
        return "stop"

    # -------------------------------------------------
    # SESSION UPDATE (NEW CORE ADDITION)
    # -------------------------------------------------
    session_manager.set_generated_audio(output_path)

    # -------------------------------------------------
    # UI UPDATE
    # -------------------------------------------------
    if hasattr(frame, "top_panel"):
        frame.top_panel.set_converted_audio(output_path)

    # -------------------------------------------------
    # SUCCESS MESSAGE
    # -------------------------------------------------
    wx.MessageBox(
        "Audio converted successfully!",
        "Success",
        wx.OK | wx.ICON_INFORMATION
    )

    return "next"


'''


'''
def step(context):

    frame = wx.GetTopLevelWindows()[0]

    # -------------------------------------------------
    # GET LOADED AUDIO
    # -------------------------------------------------
    input_path = (
        session_manager
        .get_loaded_audio()
    )

    if not input_path:

        wx.MessageBox(
            "No audio loaded.",
            "Error",
            wx.OK | wx.ICON_ERROR
        )

        return "stop"

    # -------------------------------------------------
    # EXISTING UNSAVED RESULT CHECK
    # -------------------------------------------------
    existing_result = (
        session_manager.get_result(
            "converted_audio"
        )
    )

    if (
        existing_result
        and session_manager
        .has_unsaved_work()
    ):

        choice = wx.MessageBox(
            "Unsaved converted audio exists.\n\n"
            "Continue and overwrite it?",
            "Overwrite Conversion?",
            (
                wx.YES_NO
                | wx.CANCEL
                | wx.ICON_WARNING
            )
        )

        # CANCEL
        if choice == wx.CANCEL:
            return "stop"

        # NO
        if choice == wx.NO:
            return "stop"

        # YES
        session_manager.mark_discarded(
            "converted_audio"
        )

        session_manager.clear_result(
            "converted_audio"
        )

    # -------------------------------------------------
    # FILE TYPE
    # -------------------------------------------------
    ext = os.path.splitext(
        input_path
    )[1].lower()

    # -------------------------------------------------
    # OUTPUT PATH
    # -------------------------------------------------
    root = os.path.dirname(
        os.path.dirname(__file__)
    )

    output_path = os.path.join(
        root,
        "temp_output.wav"
    )

    # =================================================
    # WAV → COPY
    # =================================================
    if ext == ".wav":

        try:

            shutil.copy2(
                input_path,
                output_path
            )

        except Exception as e:

            wx.MessageBox(
                (
                    "Copy failed:\n"
                    + str(e)
                ),
                "Error",
                wx.OK
                | wx.ICON_ERROR
            )

            return "stop"

    # =================================================
    # MP3 → C++ CONVERTER
    # =================================================
    elif ext == ".mp3":

        binary_path = os.path.join(
            root,
            "audio_converter"
        )

        try:

            result = subprocess.run(
                [
                    binary_path,
                    input_path,
                    output_path
                ],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:

                wx.MessageBox(
                    (
                        "Conversion failed:\n"
                        + result.stderr
                    ),
                    "Error",
                    wx.OK
                    | wx.ICON_ERROR
                )

                return "stop"

        except Exception as e:

            wx.MessageBox(
                (
                    "Failed to run "
                    "converter:\n"
                    + str(e)
                ),
                "Error",
                wx.OK
                | wx.ICON_ERROR
            )

            return "stop"

    # =================================================
    # UNSUPPORTED
    # =================================================
    else:

        wx.MessageBox(
            "Unsupported format.",
            "Error",
            wx.OK
            | wx.ICON_ERROR
        )

        return "stop"

    # -------------------------------------------------
    # SESSION UPDATE
    # -------------------------------------------------
    session_manager.add_result(
        "converted_audio",
        output_path
    )

    # -------------------------------------------------
    # UI UPDATE
    # -------------------------------------------------
    if hasattr(
        frame,
        "top_panel"
    ):

        frame.top_panel.set_converted_audio(
            output_path
        )

    # -------------------------------------------------
    # SUCCESS
    # -------------------------------------------------
    wx.MessageBox(
        "Audio converted successfully!",
        "Success",
        wx.OK
        | wx.ICON_INFORMATION
    )

    return "next"

'''




def step(context):

    frame = wx.GetTopLevelWindows()[0]

    # -------------------------------------------------
    # GET LOADED AUDIO (SOURCE OF TRUTH)
    # -------------------------------------------------
    input_path = session_manager.get_loaded_audio()

    if not input_path:

        wx.MessageBox(
            "No audio loaded.",
            "Error",
            wx.OK | wx.ICON_ERROR
        )

        return "stop"

    # -------------------------------------------------
    # CHECK EXISTING RESULT
    # -------------------------------------------------
    existing = session_manager.get_result("converted_audio")

    if existing:

        choice = wx.MessageBox(
            "A converted audio already exists.\n\nOverwrite it?",
            "Confirm Overwrite",
            wx.YES_NO | wx.CANCEL | wx.ICON_WARNING
        )

        if choice != wx.YES:
            return "stop"

    # -------------------------------------------------
    # FILE TYPE
    # -------------------------------------------------
    ext = os.path.splitext(input_path)[1].lower()

    # -------------------------------------------------
    # OUTPUT PATH (TEMP)
    # -------------------------------------------------
    root = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(root, "temp_output.wav")

    # =================================================
    # WAV → COPY
    # =================================================
    if ext == ".wav":

        try:
            shutil.copy2(input_path, output_path)

        except Exception as e:
            wx.MessageBox(
                f"Copy failed:\n{str(e)}",
                "Error",
                wx.OK | wx.ICON_ERROR
            )
            return "stop"

    # =================================================
    # MP3 → C++ CONVERTER
    # =================================================
    elif ext == ".mp3":

        binary_path = os.path.join(root, "audio_converter")

        try:
            result = subprocess.run(
                [binary_path, input_path, output_path],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:

                wx.MessageBox(
                    "Conversion failed:\n" + result.stderr,
                    "Error",
                    wx.OK | wx.ICON_ERROR
                )

                return "stop"

        except Exception as e:

            wx.MessageBox(
                "Converter error:\n" + str(e),
                "Error",
                wx.OK | wx.ICON_ERROR
            )

            return "stop"

    else:

        wx.MessageBox(
            "Unsupported format.",
            "Error",
            wx.OK | wx.ICON_ERROR
        )

        return "stop"

    # -------------------------------------------------
    # SESSION UPDATE (SINGLE SOURCE OF TRUTH)
    # -------------------------------------------------
    session_manager.set_result(
        "converted_audio",
        output_path
    )

    # -------------------------------------------------
    # UI SYNC (NO DIRECT STATE WRITING)
    # -------------------------------------------------
    if hasattr(frame, "top_panel"):
        frame.top_panel.refresh_from_session()

    # -------------------------------------------------
    # SUCCESS
    # -------------------------------------------------
    wx.MessageBox(
        "Audio converted successfully!",
        "Success",
        wx.OK | wx.ICON_INFORMATION
    )

    return "next"