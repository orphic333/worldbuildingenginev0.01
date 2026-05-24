from .constants import SPECIALIZATIONS, SPECIALIZATION_DESC
from .entities import Hero, Guardian, Builder


# =========================
# UNIT MANAGEMENT
# =========================

def recruit_hero(heroes):
    """
    Interactive hero creation. Player names the hero and picks a specialization.
    """

    hero_id = len(heroes) + 1

    name = input(
        "\nEnter hero name: "
    ).strip()

    if not name:

        print("A hero must have a name.")

        return recruit_hero(heroes)

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

    heroes.append(hero)

    print(
        f"\n--- {name} the {specialization} has arrived! ---"
    )

    return hero


def recruit_guardian(guardians): #should be removed.
    """
    Interactive guardian creation.
    """

    guardian_id = len(guardians) + 1

    name = input(
        "\nEnter guardian name: "
    ).strip()

    if not name:

        print("A guardian must have a name.")

        return recruit_guardian(guardians)

    guardian = Guardian(guardian_id, name)

    guardians.append(guardian)

    print(
        f"\n--- {name} the Guardian has arrived! ---"
    )

    return guardian


def recruit_builder(builders):
    """
    Interactive builder creation.
    """

    builder_id = len(builders) + 1

    name = input(
        "\nEnter builder name: "
    ).strip()  #builders don't need names, but they do need ID's. I need to make ID's much more definitive across board.

    if not name:

        print("A builder must have a name.")

        return recruit_builder(builders)

    builder = Builder(builder_id, name)

    builders.append(builder)

    print(
        f"\n--- {name} the Builder has arrived! ---"
    )

    return builder
