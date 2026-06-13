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

    hero = world_data.create_hero(name, specialization)

    print(
        f"\n--- {name} the {specialization} has arrived! ---"
    )

    return hero


def recruit_builder(world_data: DungeonWorld) -> Builder:
    """
    Interactive builder creation.
    """

    builder = world_data.create_builder()

    print(
        f"\n--- Builder #{builder.unit_id} has arrived! ---"
    )

    return builder
