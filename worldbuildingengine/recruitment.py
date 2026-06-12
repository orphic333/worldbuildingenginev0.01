from __future__ import annotations

from .constants import SPECIALIZATIONS, SPECIALIZATION_DESC
from .entities import Hero, Builder, DungeonWorld


# =========================
# UNIT MANAGEMENT
# =========================

def recruit_hero(world_data: DungeonWorld) -> Hero:
    """
    Interactive hero creation. Player names the hero and picks a specialization.
    """

    hero_id = world_data.get_next_unit_id()

    while True:

        name = input(
            "\nEnter hero name: "
        ).strip()

        if name:

            break

        print("A hero must have a name.")

    print("\nChoose a specialization:")

    for i, spec in enumerate(
        SPECIALIZATIONS,
        start=1
    ):

        print(
            f"  {i}. "
            f"{SPECIALIZATION_DESC[spec]}"
        )

    try:

        choice = int(
            input("\nEnter choice: ")
        )

        if not (1 <= choice <= len(SPECIALIZATIONS)):
            raise IndexError("Choice index out of bounds.")

        specialization = SPECIALIZATIONS[
            choice - 1
        ]

    except (ValueError, IndexError):

        print("Invalid choice. Defaulting to Prospector.")

        specialization = "Prospector"

    hero = Hero(hero_id, name, specialization)

    world_data.heroes.append(hero)

    print(
        f"\n--- {name} the {specialization} has arrived! ---"
    )

    return hero


def recruit_builder(world_data: DungeonWorld) -> Builder:
    """
    Interactive builder creation.
    """

    builder_id = world_data.get_next_unit_id()

    while True:

        name = input(
            "\nEnter builder name: "
        ).strip()

        if name:

            break

        print("A builder must have a name.")

    builder = Builder(builder_id, name)

    world_data.builders.append(builder)

    print(
        f"\n--- {name} the Builder has arrived! ---"
    )

    return builder
