from .constants import MAX_LEVEL, Resource
from .display import (
    display_random_level, display_specific_level,
)
from .entities import Expedition
from .recruitment import recruit_hero, recruit_guardian, recruit_builder


# =========================
# ORACLE SYSTEM
# =========================

def process_user_command(
    command,
    world_data,
    heroes,
    guardians,
    builders
):
    """
    Process oracle commands including unit management.
    """

    cleaned_command = command.lower().strip()

    if cleaned_command == "exit":

        print(
            "Closing the Vault. "
            "Goodbye, Architect."
        )

        return False

    elif cleaned_command == "random":

        display_random_level(world_data)

        return True

    elif cleaned_command == "recruit":

        print("\nChoose unit type:")
        print("  1. Hero")
        print("  2. Guardian")
        print("  3. Builder")

        unit_choice = input(
            "\nEnter choice: "
        ).strip()

        if unit_choice == "1":

            recruit_hero(heroes)

        elif unit_choice == "2":

            recruit_guardian(guardians)

        elif unit_choice == "3":

            recruit_builder(builders)

        else:

            print("Invalid choice.")

        return True

    elif cleaned_command == "heroes":

        has_any = heroes or guardians or builders

        if not has_any:

            print("No units have been recruited yet.")

        else:

            print("\n--- RECRUITED UNITS ---")

            if heroes:

                print("\n  Heroes:")

                for hero in heroes:

                    print(
                        f"    #{hero.unit_id} {hero.name} - "
                        f"Lvl {hero.level} {hero.specialization}"
                    )

                    print(
                        f"      HP:{hero.health:.0f} "
                        f"ST:{hero.stamina:.0f} "
                        f"SN:{hero.sanity:.0f} "
                        f"| {'Alive' if hero.is_alive else 'Dead'}"
                    )

            if guardians:

                print("\n  Guardians:")

                for guard in guardians:

                    print(
                        f"    #{guard.unit_id} {guard.name} - "
                        f"Power {guard.power}"
                    )

                    print(
                        f"      HP:{guard.health:.0f} "
                        f"| {'Alive' if guard.is_alive else 'Dead'}"
                    )

            if builders:

                print("\n  Builders:")

                for builder in builders:

                    print(
                        f"    #{builder.unit_id} {builder.name} - "
                        f"Speed {builder.build_speed}"
                    )

                    print(
                        f"      HP:{builder.health:.0f} "
                        f"| {'Alive' if builder.is_alive else 'Dead'}"
                    )

        return True

    elif cleaned_command.startswith("hero "):

        try:

            hero_id = int(
                cleaned_command.split(" ")[1]
            )

            found = None

            for h in heroes:

                if h.unit_id == hero_id:

                    found = h

                    break

            if found:

                found.display_status()

            else:

                print(f"No hero with ID {hero_id}.")

        except (ValueError, IndexError):

            print("Usage: hero <id>")

        return True

    elif cleaned_command == "zones":

        if not world_data.known_zones:

            print("No zones discovered.")

        else:

            print("\n--- KNOWN ZONES ---")

            for zone_id in world_data.known_zones:

                zone = world_data.zones[zone_id]

                print(
                    f"  Zone {zone.zone_id}: "
                    f"{zone.name} "
                    f"(Tier {zone.tier}, "
                    f"Danger {zone.danger_rating})"
                )

        return True

    elif cleaned_command == "tick":

        world_data.tick(
            heroes, guardians, builders
        )

        return True

    elif cleaned_command == "expeditions":

        if not world_data.active_expeditions:

            print("No active expeditions.")

        else:

            print("\n--- ACTIVE EXPEDITIONS ---")

            for exp in world_data.active_expeditions:

                print(
                    f"  {exp.hero.name} -> "
                    f"{exp.target_zone.name} "
                    f"(Tier {exp.target_zone.tier})"
                )

                print(
                    f"    Turn {exp.turns_elapsed} / "
                    f"{exp.duration_turns} "
                    f"| {exp.status}"
                )

        return True

    elif cleaned_command == "stockpile":

        print("\n--- STOCKPILE ---")

        for resource in Resource:

            print(
                f"  {resource.value}: "
                f"{world_data.stockpile[resource]}"
            )

        return True

    elif cleaned_command.startswith("send "):

        parts = cleaned_command.split()

        if len(parts) != 4:

            print("Usage: send <hero_id> <zone_id> <duration>")

        else:

            try:

                hero_id = int(parts[1])

                zone_id = int(parts[2])

                duration = int(parts[3])

                found_hero = None

                for h in heroes:

                    if h.unit_id == hero_id:

                        found_hero = h

                        break

                if found_hero is None:

                    print(f"No hero with ID {hero_id}.")

                elif not found_hero.is_alive:

                    print(
                        f"{found_hero.name} is dead "
                        f"and cannot be sent."
                    )

                elif found_hero.current_zone is not None:

                    print(
                        f"{found_hero.name} is already "
                        f"on an expedition."
                    )

                elif zone_id not in world_data.zones:

                    print(
                        f"No zone with ID {zone_id}."
                    )

                else:

                    target = world_data.zones[zone_id]

                    found_hero.current_zone = zone_id

                    expedition = Expedition(
                        hero=found_hero,
                        target_zone=target,
                        world=world_data,
                        duration_turns=duration,
                    )

                    world_data.active_expeditions.append(
                        expedition
                    )

                    print(
                        f"\n--- {found_hero.name} dispatched "
                        f"to {target.name} "
                        f"for {duration} turns! ---"
                    )

            except (ValueError, IndexError):

                print("Usage: send <hero_id> <zone_id> <duration>")

        return True

    elif cleaned_command.isdigit():

        level_number = int(
            cleaned_command
        )

        display_specific_level(
            world_data,
            level_number
        )

        return True

    else:

        print(
            "The Oracle does not understand."
        )

        return True


def run_oracle_system(world_data, heroes, guardians, builders):
    """
    Main interactive command loop with unit management and zones.
    """

    print("\n--- ORACLE SYSTEM ACTIVE ---")

    print(
        f"Options: Type a level number "
        f"(1-{MAX_LEVEL}), "
        f"'random', "
        f"'recruit', "
        f"'heroes', "
        f"'hero <id>', "
        f"'zones', "
        f"'tick', "
        f"'send <hero_id> <zone_id> <duration>', "
        f"'expeditions', "
        f"'stockpile', "
        f"or 'exit'."
    )

    is_running = True

    while is_running:

        user_command = input(
            "\nEnter Command: "
        )

        is_running = process_user_command(
            user_command,
            world_data,
            heroes,
            guardians,
            builders
        )
