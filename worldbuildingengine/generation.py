import random

from .constants import (
    ADJECTIVES, MATERIALS, LOCATIONS,
    TERRAIN_TYPES, ZONE_MODIFIERS, MAX_LEVEL,
)
from .entities import DungeonLevel, WorldZone, DungeonWorld


# =========================
# CORE CALCULATIONS
# =========================

def calculate_aether_density(level):

    density = 1.8 * level**2 + 2 * level + 16

    return round(density, 3)


def calculate_guardian_power(level):

    return round(level * 1.1, 3)


# =========================
# LEVEL GENERATION
# =========================

def generate_level_name():

    adjective = random.choice(ADJECTIVES)
    material = random.choice(MATERIALS)
    location = random.choice(LOCATIONS)

    return f"The {adjective} {material} {location}"


def create_level_data(level_number):

    return DungeonLevel(
        level_id=level_number,
        name=generate_level_name(),
        aether_density=calculate_aether_density(level_number),
        guardian_power=calculate_guardian_power(level_number),
    )


def generate_dungeon_world(max_level=MAX_LEVEL):

    levels = {
        level: create_level_data(level)
        for level in range(1, max_level + 1)
    }

    zone_id_counter = 1
    zones = {}
    known_zones = []

    tier_configs = [
        (1, 5),
        (2, 3),
        (3, 2),
    ]

    for tier, count in tier_configs:

        for _ in range(count):

            modifier = random.choice(ZONE_MODIFIERS)
            terrain = random.choice(TERRAIN_TYPES)
            danger = round(tier * 10.0 + random.uniform(0, 5), 3)

            zone = WorldZone(
                zone_id=zone_id_counter,
                name=f"{modifier} {terrain}",
                tier=tier,
                danger_rating=danger,
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
    )
