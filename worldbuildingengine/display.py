import random

from .constants import MAX_LEVEL


# =========================
# DISPLAY HELPERS
# =========================

def display_save_files(save_files):
    """
    Display available save files.
    """

    print("\n--- AVAILABLE WORLDS ---")

    if not save_files:
        print("No worlds found.")
        return

    for index, save_name in enumerate(
        save_files,
        start=1
    ):
        print(f"{index}. {save_name}")


def display_level_summary(level_data):
    """
    Display formatted level data.
    """

    print(
        f"Level {level_data.level_id}: "
        f"{level_data.name}"
    )

    print(
        f"  > Aether: "
        f"{level_data.aether_density} units"
    )

    print(
        f"  > Guardian: "
        f"Pwr Lvl {level_data.guardian_power}"
    )

    print("-" * 30)


def display_world_overview(world_data):
    """
    Display all dungeon levels.
    """

    print("\n--- THE GREAT DESCENT ---")

    for level_data in world_data.levels.values():
        display_level_summary(level_data)


def display_random_level(world_data):
    """
    Display a random level.
    """

    random_level_number = random.randint(
        1,
        MAX_LEVEL
    )

    level_data = world_data.levels[random_level_number]

    print(
        f"\n[DISCOVERY] "
        f"Level {random_level_number}: "
        f"{level_data.name}"
    )

    print(
        f"Stats: "
        f"Aether {level_data.aether_density} | "
        f"Guardian {level_data.guardian_power}"
    )


def display_specific_level(
    world_data,
    level_number
):
    """
    Display chosen level data.
    """

    if not 1 <= level_number <= MAX_LEVEL:

        print(
            f"The Abyss only goes "
            f"to Level {MAX_LEVEL}."
        )

        return

    level_data = world_data.levels[level_number]

    print(
        f"\n[FOUND] "
        f"{level_data.name}"
    )

    print(
        f"Logic Specs: "
        f"Density {level_data.aether_density} | "
        f"Power {level_data.guardian_power}"
    )
