from __future__ import annotations

import random

from .constants import (
    ADJECTIVES, MATERIALS, LOCATIONS,
    TERRAIN_TYPES, ZONE_MODIFIERS, MAX_LEVEL,
    Resource,
)
from .entities import DungeonLevel, WorldZone, DungeonWorld


# =========================
# CORE CALCULATIONS
# =========================

def calculate_aether_density(level: int) -> float:

    density = 1.8 * level**2 + 2 * level + 16

    return round(density, 3)


def calculate_guardian_power(level: int) -> float:

    return round(level * 1.1, 3)


def generate_level_name() -> str:

    adjective = random.choice(ADJECTIVES)
    material = random.choice(MATERIALS)
    location = random.choice(LOCATIONS)

    return f"The {adjective} {material} {location}"


def create_level_data(level_number: int) -> DungeonLevel:

    return DungeonLevel(
        level_id=level_number,
        name=generate_level_name(),
        aether_density=calculate_aether_density(level_number),
        guardian_power_level=calculate_guardian_power(level_number),
        resource_nodes={
            Resource.AETHER_CRYSTALS: int(
                calculate_aether_density(level_number) * 0.5
            ),
            Resource.COPPER: random.randint(0, 5),  #fix resource definitions and distributions.
            Resource.STONE: random.randint(2, 10),   #Resources could be renewable, foundational types like varieties of rocks and ores in area around the level.
            Resource.HARD_ROCK: random.randint(1, 5),
            Resource.SOFT_ROCK: random.randint(0, 3),
            Resource.IRON: random.randint(3, 8),
        },
    )


def generate_dungeon_world(max_level: int = MAX_LEVEL) -> DungeonWorld:

    levels = {
        level: create_level_data(level)
        for level in range(1, max_level + 1)
    }

    zone_id_counter = 1
    zones = {}
    known_zones = []

    tier_configs = [
        (1, 3),
        (2, 4),
        (3, 3),
    ]

    initial_event_zone_ids = []

    for tier, count in tier_configs:

        for _ in range(count):

            modifier = random.choice(ZONE_MODIFIERS)
            terrain = random.choice(TERRAIN_TYPES)
            danger = round(tier * 10.0 + random.uniform(0, 5), 3)

            if tier == 1:

                zone_resources = {
                    Resource.WOOD: random.randint(5, 15), #NEED TO FIX ZONE RESOURCE DISTRIBUTIONS ACC. TO TIERS
                    Resource.FIBRE: random.randint(3, 8),
                    Resource.KNOWLEDGE: random.randint(1, 5),
                }
                initial_event_zone_ids.append(zone_id_counter)

            elif tier == 2:

                zone_resources = {
                    Resource.COPPER: random.randint(10, 25),     #NEED TO FIX ZONE RESOURCE DISTRIBUTIONS ACC. TO TIERS
                    Resource.IRON: random.randint(5, 15),
                    Resource.MEDICINAL_PLANTS: random.randint(2, 8),
                    Resource.KNOWLEDGE: random.randint(5, 12),
                }

            else:

                zone_resources = {                              #NEED TO FIX ZONE RESOURCE DISTRIBUTIONS ACC. TO TIERS
                    Resource.RARE_METALS: random.randint(8, 20),
                    Resource.KNOWLEDGE: random.randint(10, 20),
                }

            zone = WorldZone(
                zone_id=zone_id_counter,
                name=f"{modifier} {terrain}",
                tier=tier,
                danger_rating=danger,
                resource_nodes=zone_resources,
            )

            zones[zone_id_counter] = zone
            zone_id_counter += 1

    # Discover first 2 Tier 1 zones
    discovered = 0

    for zone in zones.values():

        if zone.tier == 1 and discovered < 2:

            zone.is_discovered = True
            known_zones.append(zone.zone_id)
            discovered += 1

    return DungeonWorld(
        levels=levels,
        zones=zones,
        known_zones=known_zones,
        event_zone_ids=initial_event_zone_ids,
    )
