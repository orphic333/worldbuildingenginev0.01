from __future__ import annotations

from .display import display_save_files, display_world_overview
from .entities import DungeonWorld
from .generation import generate_dungeon_world
from .save_load import (
    save_dungeon_world, load_dungeon_world,
    list_save_files, is_valid_save_name,
)
from .oracle import run_oracle_system


# =========================
# WORLD INITIALIZATION
# =========================

def create_new_world() -> tuple[DungeonWorld, str]:
    """
    Create and save a new dungeon world.
    """

    while True:

        save_name = input(
            "\nEnter new world name: "
        ).strip()

        if not save_name:

            print("World name cannot be empty.")

        elif not is_valid_save_name(save_name):

            print(
                "World name must only contain letters, "
                "digits, spaces, hyphens, and underscores."
            )

        else:

            break

    dungeon_world = generate_dungeon_world()

    save_dungeon_world(
        dungeon_world,
        save_name
    )

    print("--- NEW WORLD GENERATED ---")

    return dungeon_world, save_name


def select_existing_world(save_files: list[str]) -> tuple[DungeonWorld, str]:
    """
    Load a selected save file.
    """

    while True:

        try:

            selection = int(
                input("\nSelect save number: ")
            )

            if not (1 <= selection <= len(save_files)):
                raise IndexError("Selection index out of bounds.")

            selected_save = save_files[
                selection - 1
            ]

            dungeon_world = load_dungeon_world(
                selected_save
            )

            return dungeon_world, selected_save

        except (
            ValueError,
            IndexError
        ):

            print("Invalid selection.")


def initialize_world() -> tuple[DungeonWorld, str]:
    """
    Handle startup world selection.
    """

    save_files = list_save_files()

    display_save_files(save_files)

    print("\nOptions:")
    print("1. Load Existing World")
    print("2. Create New World")

    while True:

        choice = input(
            "\nEnter choice: "
        ).strip()

        if choice == "1":

            if not save_files:

                print("No saves available.")

                return create_new_world()

            return select_existing_world(
                save_files
            )

        elif choice == "2":

            return create_new_world()

        else:

            print("Invalid option.")


# =========================
# MAIN PROGRAM
# =========================

def main() -> None:

    dungeon_world, save_name = (
        initialize_world()
    )

    print(
        f"\n--- ACTIVE WORLD: "
        f"{save_name} ---"
    )

    display_world_overview(
        dungeon_world
    )

    run_oracle_system(
        dungeon_world
    )


if __name__ == "__main__":
    main()
