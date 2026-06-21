# =====================================================
# SessionManager.py
# Handles global application session state
# (RAM session + persistent cache)
# =====================================================

import os
import json


# =====================================================
# SessionItem
# Represents one temporary/generated result
# =====================================================
class SessionItem:

    def __init__(self, item_type, path=None):
        self.item_type = item_type
        self.path = path

        # save states:
        # None | "undecided" | "saved" | "discarded"
        self.save_state = None

        # future use (pipeline / cleanup control)
        self.delete_on_exit = True

    # -------------------------------------------------
    # Set result path
    # -------------------------------------------------
    def set_path(self, path):
        self.path = path
        self.save_state = "undecided"

    # -------------------------------------------------
    # Save state helpers
    # -------------------------------------------------
    def mark_saved(self):
        self.save_state = "saved"

    def mark_discarded(self):
        self.save_state = "discarded"

    def mark_unsaved(self):
        self.save_state = "undecided"

    # -------------------------------------------------
    # State checks
    # -------------------------------------------------
    def exists(self):
        return self.path is not None

    def is_unsaved(self):
        return self.exists() and self.save_state == "undecided"

    def clear(self):
        self.path = None
        self.save_state = None


# =====================================================
# SessionManager (Singleton)
# =====================================================
class SessionManager:

    _instance = None

    # -------------------------------------------------
    # Singleton access
    # -------------------------------------------------
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    # -------------------------------------------------
    # INIT
    # -------------------------------------------------
    def _init(self):

        # -----------------------------
        # Loaded audio (source)
        # -----------------------------
        self.loaded_audio_path = None

        # -----------------------------
        # Generated results
        # -----------------------------
        self.generated_results = {
            "converted_audio": SessionItem("converted_audio")
        }

        # -----------------------------
        # Cache system
        # -----------------------------
        self.cache = {
            "last_open_audio_folder": None,
            "last_save_audio_folder": None
        }

        self._load_cache()

    # =================================================
    # CACHE FILE PATH
    # =================================================
    def _get_cache_file_path(self):

        root = os.path.dirname(__file__)

        config_folder = os.path.join(root, "config")
        os.makedirs(config_folder, exist_ok=True)

        return os.path.join(config_folder, "session_cache.json")

    # =================================================
    # LOAD CACHE
    # =================================================
    def _load_cache(self):

        try:
            cache_file = self._get_cache_file_path()

            if os.path.exists(cache_file):
                with open(cache_file, "r") as f:
                    data = json.load(f)
                self.cache.update(data)

        except Exception:
            pass

    # =================================================
    # SAVE CACHE
    # =================================================
    def _save_cache(self):

        try:
            cache_file = self._get_cache_file_path()

            with open(cache_file, "w") as f:
                json.dump(self.cache, f, indent=4)

        except Exception:
            pass

    # =================================================
    # AUDIO LOADING
    # =================================================
    def set_loaded_audio(self, path):
        self.loaded_audio_path = path

    def get_loaded_audio(self):
        return self.loaded_audio_path

    def has_loaded_audio(self):
        return self.loaded_audio_path is not None

    def clear_loaded_audio(self):
        self.loaded_audio_path = None

    # =================================================
    # RESULT SYSTEM (PRIMARY API)
    # =================================================
    def add_result(self, name, path):

        if name not in self.generated_results:
            self.generated_results[name] = SessionItem(name)

        self.generated_results[name].set_path(path)

    def set_result(self, name, path):
        """Compatibility alias (used by newer modules)"""
        self.add_result(name, path)

    def get_result(self, name):

        item = self.generated_results.get(name)
        if item:
            return item.path

        return None

    def result_exists(self, name):
        return (
            name in self.generated_results
            and self.generated_results[name].exists()
        )

    # =================================================
    # SAVE / DISCARD
    # =================================================
    def mark_saved(self, name):
        item = self.generated_results.get(name)
        if item:
            item.mark_saved()

    def mark_discarded(self, name):
        item = self.generated_results.get(name)
        if item:
            item.mark_discarded()

    def clear_result(self, name):
        item = self.generated_results.get(name)
        if item:
            item.clear()

    # =================================================
    # UNSAVED WORK CHECK
    # =================================================
    def has_unsaved_work(self):

        for item in self.generated_results.values():
            if item.is_unsaved():
                return True

        return False

    def is_transient(self):
        return self.has_unsaved_work()

    def is_complete(self):
        return not self.has_unsaved_work()

    # =================================================
    # CACHE HELPERS
    # =================================================
    def get_last_open_folder(self):
        return self.cache.get("last_open_audio_folder")

    def set_last_open_folder(self, path):
        self.cache["last_open_audio_folder"] = path
        self._save_cache()

    def get_last_save_folder(self):
        return self.cache.get("last_save_audio_folder")

    def set_last_save_folder(self, path):
        self.cache["last_save_audio_folder"] = path
        self._save_cache()

    # =================================================
    # FULL RESET
    # =================================================
    def clear_session(self):

        self.loaded_audio_path = None

        for item in self.generated_results.values():
            item.clear()


# -----------------------------------------------------
# GLOBAL INSTANCE
# -----------------------------------------------------
session_manager = SessionManager()