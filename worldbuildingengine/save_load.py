import json
import os

from .constants import SAVE_FOLDER
from .entities import DungeonLevel, DungeonWorld


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
    Save world data to JSON.
    """

    filepath = get_save_path(save_name)

    world_data.name = save_name

    with open(filepath, "w") as file:
        json.dump(world_data.to_dict(), file, indent=4)

    print(f"--- WORLD '{save_name}' SAVED ---")


def load_dungeon_world(save_name):
    """
    Load a saved dungeon world.
    """

    filepath = get_save_path(save_name)

    try:

        with open(filepath, "r") as file:
            data = json.load(file)

        # Backward compat: pre-refactor saves use flat "Level N" keys
        if isinstance(data, dict) and any(
            k.startswith("Level ") for k in data
        ):

            levels = {}

            for key, level_data in data.items():

                levels[level_data["level_id"]] = DungeonLevel(
                    level_id=level_data["level_id"],
                    name=level_data["level_name"],
                    aether_density=level_data["aether_density"],
                    guardian_power=level_data["guardian_level"],
                )

            world_data = DungeonWorld(levels=levels)

        else:

            world_data = DungeonWorld.from_dict(data)

        print(f"--- WORLD '{save_name}' LOADED ---")

        return world_data

    except FileNotFoundError:

        return None
