from .constants import Resource, INITIAL_SUPPLIES
from typing import Any
# The active version of the world save schema expected by the game codebase.
CURRENT_SCHEMA_VERSION = 3

def migrate_v1_to_v2(data:dict[str,Any])->dict[str,Any]:
    """
    Migrates a legacy flat level save (v1) to the centralized container save (v2).
    In v1, the save file is a flat dictionary of Level names/data.
    In v2, it's a DungeonWorld container.
    """
    print("  [Migration] Upgrading save format: v1 to v2")

    # Reconstruct levels from flat "Level N" keys
    levels = {}
    for key, lvl_data in data.items():
        if key.startswith("Level "):
            lvl_id = lvl_data.get("level_id")
            levels[str(lvl_id)] = {
                "level_id": lvl_id,
                "name": lvl_data.get("level_name"),
                "aether_density": lvl_data.get("aether_density"),
                "guardian_power_level": lvl_data.get("guardian_level"),
                "resource_nodes": lvl_data.get("resource_nodes", {}),
                "structural_mods": lvl_data.get("structural_mods", []),
                "active_events": lvl_data.get("active_events", []),
                "is_explored": lvl_data.get("is_explored", False)
            }

    # Return a clean v2 container representation
    return {
        "schema_version": 2,
        "name": "Migrated World",
        "turn": 0,
        "next_unit_id": 1,
        "levels": levels,
        "zones": {},
        "known_zones": [],
        "heroes": [],
        "guardians": [],
        "builders": [],
        "active_expeditions": [],
        "stockpile": {r.value: 0 for r in Resource}
    }


def migrate_v2_to_v3(data: dict[str, Any]) -> dict[str, Any]:
    """Seed expedition_supplies for v2 saves that lack the field."""
    print("  [Migration] Seeding expedition supplies: v2 to v3")
    data.setdefault("expedition_supplies", 30)
    data["schema_version"] = 3
    return data

# Dictionary mapping source version to the corresponding migration function
MIGRATION_PIPELINE = {
    1: migrate_v1_to_v2,
    2: migrate_v2_to_v3,
}

def migrate_data(data:dict)->dict:
    """
    Sequentially runs schema upgrade migrations on loaded dict data
    until it matches CURRENT_SCHEMA_VERSION.
    """
    # 1. Detect version.
    # If the root is a flat "Level N" dictionary, it's v1.
    # Otherwise, it should have a schema_version key.
    if isinstance(data, dict) and any(k.startswith("Level ") for k in data):
        version = 1
    else:
        version = data.get("schema_version", 2)  # Default to v2 if not v1 and no version key

    if version == CURRENT_SCHEMA_VERSION:
        return data

    print(f"--- STARTING SAVE SCHEMA UPGRADE (Current: v{version} -> Target: v{CURRENT_SCHEMA_VERSION}) ---")

    while version < CURRENT_SCHEMA_VERSION:
        migration_func = MIGRATION_PIPELINE.get(version)
        if not migration_func:
            raise ValueError(f"No migration pipeline registered for schema version {version}")

        data = migration_func(data)
        version = data.get("schema_version")

    print("--- SAVE SCHEMA UPGRADE COMPLETED ---")
    return data
