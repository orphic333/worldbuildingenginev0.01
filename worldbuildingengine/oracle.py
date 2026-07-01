from __future__ import annotations

from .constants import MAX_LEVEL, Resource, CONSUMABLE_RESOURCES
from .display import (
    display_random_level, display_specific_level,
    display_world_zones, display_aether_nodes,
)
from .entities import Expedition, DungeonWorld
from .recruitment import recruit_hero, recruit_builder
from .save_load import save_dungeon_world


# =========================
# ORACLE SYSTEM
# =========================

def process_user_command(
    command: str,
    world_data: DungeonWorld
) -> bool:
    """
    Process oracle commands including unit management.
    """

    cleaned_command = command.lower().strip()

    if cleaned_command == "exit":

        print(
            "Closing the Vault. "
            "Goodbye, Architect."
        )

        save_dungeon_world(world_data, world_data.name)

        return False

    elif cleaned_command == "save":

        save_dungeon_world(world_data, world_data.name)

        return True

    elif cleaned_command == "random":

        display_random_level(world_data)

        return True

    elif cleaned_command == "recruit":

        print("\nChoose unit type:")
        print("  1. Hero")
        print("  2. Builder")

        unit_choice = input(
            "\nEnter choice: "
        ).strip()

        if unit_choice == "1":

            recruit_hero(world_data)

        elif unit_choice == "2":

            recruit_builder(world_data)

        else:

            print("Invalid choice.")

        return True

    elif cleaned_command == "heroes":

        has_any = world_data.heroes or world_data.guardians or world_data.builders

        if not has_any:

            print("No units have been recruited yet.")

        else:

            print("\n--- RECRUITED UNITS ---")

            if world_data.heroes:

                print("\n  Heroes:")

                for hero in world_data.heroes:

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

            if world_data.guardians:

                print("\n  Guardians:")

                for guard in world_data.guardians:

                    print(
                        f"    #{guard.unit_id} {guard.name} - "
                        f"Power {guard.power_level}"
                    )

                    print(
                        f"      HP:{guard.health:.0f} "
                        f"| {'Alive' if guard.is_alive else 'Dead'}"
                    )

            if world_data.builders:

                print("\n  Builders:")

                for builder in world_data.builders:

                    print(
                        f"    #{builder.unit_id} - "
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

            if hero_id < 0:

                print("Hero ID must be non-negative.")

            else:

                found = None

                for h in world_data.heroes:

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

        display_world_zones(world_data)

        return True

    elif cleaned_command == "tick":

        world_data.tick()
        save_dungeon_world(world_data, world_data.name)

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

        for resource in CONSUMABLE_RESOURCES:

            print(
                f"  {resource.value}: "
                f"{world_data.stockpile[resource]}"
            )

        print(
            f"\n  Expedition Supplies: "
            f"{world_data.expedition_supplies}"
        )

        return True

    elif cleaned_command.startswith("harvest "):

        parts = cleaned_command.split()
        if len(parts) != 2:
            print("Usage: harvest <level_id>")
            return True
        try:
            level_id = int(parts[1])
        except ValueError:
            print("Level ID must be a number.")
            return True

        level = world_data.levels.get(level_id)
        if level is None:
            print(f"Level {level_id} not found.")
            return True

        total = 0
        for node in level.aether_crystal_nodes:
            total += node["current"]
            node["current"] = 0

        if total > 0:
            world_data.stockpile[Resource.AETHER_CRYSTALS] += total
            print(
                f"Harvested {total} aether crystals "
                f"from level {level_id}."
            )
        else:
            print(f"No aether crystals to harvest on level {level_id}.")

        return True

    elif cleaned_command.startswith("nodes "):

        parts = cleaned_command.split()
        if len(parts) != 2:
            print("Usage: nodes <level_id>")
            return True
        try:
            level_id = int(parts[1])
        except ValueError:
            print("Level ID must be a number.")
            return True

        display_aether_nodes(world_data, level_id)
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

                if hero_id < 0 or zone_id < 0:

                    print("Hero ID and Zone ID must be non-negative.")

                elif duration <= 0:

                    print("Duration must be a positive integer.")

                else:

                    found_hero = None

                    for h in world_data.heroes:

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
                        try:
                            expedition = world_data.send_hero_on_expedition(
                                hero_id,
                                zone_id,
                                duration,
                            )
                            print(
                                f"\n--- {expedition.hero.name} dispatched "
                                f"to {expedition.target_zone.name} "
                                f"for {duration} turns! ---"
                            )
                        except ValueError as exc:
                            print(exc)

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


def run_oracle_system(world_data: DungeonWorld) -> None:
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
        f"'harvest <level_id>', "
        f"'nodes <level_id>', "
        f"'save', "
        f"or 'exit'."
    )

    is_running = True

    while is_running:

        user_command = input(
            "\nEnter Command: "
        )

        is_running = process_user_command(
            user_command,
            world_data
        )
