from .display import display_save_files, display_world_overview
from .generation import generate_dungeon_world
from .save_load import (
    save_dungeon_world, load_dungeon_world,
    list_save_files,
)
from .oracle import run_oracle_system


# =========================
# WORLD INITIALIZATION
# =========================

def create_new_world():
    """
    Create and save a new dungeon world.
    """

    save_name = input(
        "\nEnter new world name: "
    ).strip()

    if not save_name:

        print("Invalid world name.")

        return create_new_world()

    dungeon_world = generate_dungeon_world()

    save_dungeon_world(
        dungeon_world,
        save_name
    )

    print("--- NEW WORLD GENERATED ---")

    return dungeon_world, save_name


def select_existing_world(save_files):
    """
    Load a selected save file.
    """

    try:

        selection = int(
            input("\nSelect save number: ")
        )

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

        return select_existing_world(
            save_files
        )


def initialize_world():
    """
    Handle startup world selection.
    """

    save_files = list_save_files()

    display_save_files(save_files)

    print("\nOptions:")
    print("1. Load Existing World")
    print("2. Create New World")

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

        return initialize_world()


# =========================
# MAIN PROGRAM
# =========================

def main():

    dungeon_world, save_name = (
        initialize_world()
    )

    heroes = []
    guardians = []
    builders = []

    print(
        f"\n--- ACTIVE WORLD: "
        f"{save_name} ---"
    )

    display_world_overview(
        dungeon_world
    )

    run_oracle_system(
        dungeon_world,
        heroes,
        guardians,
        builders
    )


if __name__ == "__main__":
    main()
