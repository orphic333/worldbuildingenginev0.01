from .constants import SPECIALIZATIONS, SPECIALIZATION_DESC
from .entities import Hero, Guardian, Builder


# =========================
# UNIT MANAGEMENT
# =========================

def recruit_hero(world_data):
    """
    Interactive hero creation. Player names the hero and picks a specialization.
    """

    hero_id = world_data.get_next_unit_id()

    name = input(
        "\nEnter hero name: "
    ).strip()

    if not name:

        print("A hero must have a name.")

        return recruit_hero(world_data)

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


def recruit_guardian(world_data):
    """
    Interactive guardian creation.
    """

    guardian_id = world_data.get_next_unit_id()

    name = input(
        "\nEnter guardian name: "
    ).strip()

    if not name:

        print("A guardian must have a name.")

        return recruit_guardian(world_data)

    guardian = Guardian(guardian_id, name)

    world_data.guardians.append(guardian)

    print(
        f"\n--- {name} the Guardian has arrived! ---"
    )

    return guardian


def recruit_builder(world_data):
    """
    Interactive builder creation.
    """

    builder_id = world_data.get_next_unit_id()

    name = input(
        "\nEnter builder name: "
    ).strip()

    if not name:

        print("A builder must have a name.")

        return recruit_builder(world_data)

    builder = Builder(builder_id, name)

    world_data.builders.append(builder)

    print(
        f"\n--- {name} the Builder has arrived! ---"
    )

    return builder
