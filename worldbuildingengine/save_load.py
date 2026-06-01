from __future__ import annotations

import json
import os
import re

from .constants import SAVE_FOLDER
from .entities import DungeonWorld


# =========================
# SAVE SYSTEM
# =========================

def ensure_save_directory_exists() -> None:
    """
    Create save folder if missing.
    """

    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

SAVE_NAME_RE = re.compile(r"^[\w\- ]+$")


def is_valid_save_name(save_name: str) -> bool:
    """Return True if save_name is safe to use as a filename."""
    return bool(SAVE_NAME_RE.match(save_name))


def get_save_path(save_name: str) -> str:
    """
    Build full save filepath.
    """

    if not is_valid_save_name(save_name):

        raise ValueError(
            f"Invalid save name: '{save_name}'. "
            f"Use only letters, digits, spaces, hyphens, and underscores."
        )

    return os.path.join(
        SAVE_FOLDER,
        f"{save_name}.json"
    )


def list_save_files() -> list[str]:
    """
    Return all available save names.
    """

    ensure_save_directory_exists()

    save_files = os.listdir(SAVE_FOLDER)

    return [
        file.replace(".json", "")
        for file in save_files
        if file.endswith(".json")
    ]


def save_dungeon_world(world_data: DungeonWorld, save_name: str) -> None:
    """
    Save world data to JSON transactionally to prevent data corruption.
    """

    ensure_save_directory_exists()

    filepath = get_save_path(save_name)
    temp_filepath = filepath + ".tmp"

    world_data.name = save_name

    try:
        # Obtain serialized state and stamp CURRENT_SCHEMA_VERSION
        save_dict = world_data.to_dict()

        from .migrations import CURRENT_SCHEMA_VERSION
        save_dict["schema_version"] = CURRENT_SCHEMA_VERSION

        # 1. Write the save data to a temporary file
        with open(temp_filepath, "w") as file:
            json.dump(save_dict, file, indent=4)
            file.flush()
            os.fsync(file.fileno())  # Force OS buffers to write to physical storage

        # 2. Swap files atomically
        os.replace(temp_filepath, filepath)
        print(f"--- WORLD '{save_name}' SAVED TRANSACTIONALLY ---")

    except Exception as e:
        # Clean up temporary file if write fails
        if os.path.exists(temp_filepath):
            try:
                os.remove(temp_filepath)
            except OSError:
                pass
        raise e


def load_dungeon_world(save_name: str) -> DungeonWorld | None:
    """
    Load a saved dungeon world.
    """

    filepath = get_save_path(save_name)

    try:

        with open(filepath, "r") as file:
            data = json.load(file)

        # Validate top-level structure after parsing
        if not isinstance(data, dict):

            print(
                f"Corrupt save '{save_name}': "
                f"expected a dict, got {type(data).__name__}."
            )

            return None

        is_v1 = any(
            k.startswith("Level ") for k in data
        )

        is_v2 = "levels" in data

        if not (is_v1 or is_v2):

            print(
                f"Unrecognised save format '{save_name}': "
                f"missing both 'Level N' keys and 'levels' key."
            )

            return None

        # Sequentially run schema migration upgrades on raw data
        from .migrations import migrate_data
        data = migrate_data(data)

        # Instantiate from migrated save representation
        world_data = DungeonWorld.from_dict(data)

        print(f"--- WORLD '{save_name}' LOADED ---")

        return world_data

    except FileNotFoundError:

        return None

    except json.JSONDecodeError as e:

        print(
            f"Corrupt save '{save_name}': "
            f"JSON parse error at line {e.lineno}: {e.msg}"
        )

        return None

    except (KeyError, ValueError, TypeError) as e:

        print(
            f"Save '{save_name}' contains invalid data: {e}"
        )

        return None
