import json
import os

from .constants import SAVE_FOLDER
from .entities import DungeonWorld


# =========================
# SAVE SYSTEM
# =========================

def ensure_save_directory_exists():
    """
    Create save folder if missing.
    """

    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)


def get_save_path(save_name):
    """
    Build full save filepath.
    """

    return os.path.join(
        SAVE_FOLDER,
        f"{save_name}.json"
    )


def list_save_files():
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


def save_dungeon_world(world_data, save_name):
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


def load_dungeon_world(save_name:str)->dict:
    """
    Load a saved dungeon world.
    """

    filepath = get_save_path(save_name)

    try:

        with open(filepath, "r") as file:
            data = json.load(file)

        # Sequentially run schema migration upgrades on raw data
        from .migrations import migrate_data
        data = migrate_data(data)

        # Instantiate from migrated save representation
        world_data = DungeonWorld.from_dict(data)

        print(f"--- WORLD '{save_name}' LOADED ---")

        return world_data

    except FileNotFoundError:

        return None
