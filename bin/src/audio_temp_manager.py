import os
import shutil


# -------------------------------------------------
# Temp results folder
# -------------------------------------------------
def get_temp_results_folder():
    root = os.path.dirname(
        os.path.dirname(__file__)
    )

    temp_folder = os.path.join(
        root,
        "temp",
        "results"
    )

    # Create automatically if missing
    os.makedirs(
        temp_folder,
        exist_ok=True
    )

    return temp_folder


# -------------------------------------------------
# Safe filename generation
# Avoid overwrite conflicts
# -------------------------------------------------
def get_safe_output_path(
    folder,
    filename
):
    base, extension = os.path.splitext(
        filename
    )

    output_path = os.path.join(
        folder,
        filename
    )

    counter = 1

    while os.path.exists(output_path):
        output_path = os.path.join(
            folder,
            f"{base}_{counter}{extension}"
        )

        counter += 1

    return output_path


# -------------------------------------------------
# Delete temp file safely
# -------------------------------------------------
def delete_temp_file(path):
    try:
        if path and os.path.exists(path):
            os.remove(path)

    except Exception:
        pass


# -------------------------------------------------
# Copy file safely
# -------------------------------------------------
def copy_file(
    source,
    destination
):
    shutil.copy2(
        source,
        destination
    )