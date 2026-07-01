from __future__ import annotations

import random

from .constants import MAX_LEVEL
from .entities import DungeonLevel, DungeonWorld


# =========================
# DISPLAY HELPERS
# =========================

def display_save_files(save_files: list[str]) -> None:
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


def _node_summary(level: DungeonLevel) -> str:
    """Build a one-line aether crystal node summary."""
    if not level.aether_crystal_nodes:
        return ""
    total_current = sum(n["current"] for n in level.aether_crystal_nodes)
    total_max = sum(n["max_capacity"] for n in level.aether_crystal_nodes)
    count = len(level.aether_crystal_nodes)
    return f"  > Aether Nodes: {count} ({total_current}/{total_max})"


def display_level_summary(level_data: DungeonLevel) -> None:
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
        f"Pwr Lvl {level_data.guardian_power_level}"
    )

    summary = _node_summary(level_data)
    if summary:
        print(summary)

    print("-" * 30)


def display_world_overview(world_data: DungeonWorld) -> None:
    """
    Display all dungeon levels.
    """

    print("\n--- THE GREAT DESCENT ---")

    for level_data in world_data.levels.values():
        display_level_summary(level_data)


def display_random_level(world_data: DungeonWorld) -> None:   #might need to remove this thing
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
        f"Guardian {level_data.guardian_power_level}"
    )


def display_specific_level(
    world_data: DungeonWorld,
    level_number: int
) -> None:
    """
    Display chosen level data.
    """

    if not 1 <= level_number <= MAX_LEVEL:

        print(
            f"The Dungeon only goes "
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
        f"Power {level_data.guardian_power_level}"
    )

    if level_data.aether_crystal_nodes:
        print(f"\n  Aether Crystal Nodes ({len(level_data.aether_crystal_nodes)}):")
        for idx, node in enumerate(level_data.aether_crystal_nodes, 1):
            status = "full" if node["current"] >= node["max_capacity"] else "growing"
            print(
                f"    Node {idx}: {node['current']}/{node['max_capacity']} "
                f"({status}, +{node['growth_rate']}/tick)"
            )

def display_aether_nodes(
    world_data: DungeonWorld,
    level_number: int,
) -> None:
    """Show detailed aether crystal node status for a specific level."""

    if level_number not in world_data.levels:
        print(f"Level {level_number} not found.")
        return

    level = world_data.levels[level_number]

    if not level.aether_crystal_nodes:
        print(f"No aether crystal nodes on level {level_number}.")
        return

    print(f"\nLevel {level_number} - Aether Crystal Nodes:")
    total_current = 0
    total_max = 0
    for idx, node in enumerate(level.aether_crystal_nodes, 1):
        total_current += node["current"]
        total_max += node["max_capacity"]
        status = "full" if node["current"] >= node["max_capacity"] else "growing"
        print(
            f"  Node {idx}: {node['current']}/{node['max_capacity']} "
            f"({status}, +{node['growth_rate']}/tick)"
        )
    print(f"  Total: {total_current}/{total_max}")


def display_world_zones(world_data: DungeonWorld) -> None:
    """Display all known world zones and their details."""

    if not world_data.known_zones:
        print("\nNo zones discovered.")
        return

    print("\n--- KNOWN ZONES ---")

    for idx, zone_id in enumerate(world_data.known_zones, 1):
        zone = world_data.zones[zone_id]
        print(
            f"\n{idx}. Zone {zone.zone_id}: {zone.name}"
        )
        print(f"   Tier: {zone.tier}")
        print(f"   Danger Rating: {zone.danger_rating}")
        print(f"   Threat Level: {zone.threat_level}")
        if zone.event_creature_active:
            print(f"   [ACTIVE CREATURE] {zone.event_creature_name}")
        if zone.resource_nodes:
            resources = ", ".join(
                f"{r.value}: {qty}"
                for r, qty in zone.resource_nodes.items()
            )
            print(f"   Resources: {resources}")
        else:
            print("   Resources: None discovered")
