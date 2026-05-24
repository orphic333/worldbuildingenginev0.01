import enum


# =========================
# CONSTANTS
# =========================

SAVE_FOLDER = "saves"
MAX_LEVEL = 3

ADJECTIVES = [
    "Pulsing",
    "Forgotten",
    "Void-Touched",
    "Shimmering",
    "Stygian",
    "Radiant"
]

MATERIALS = [
    "Obsidian",
    "Aether-glass",
    "Bone",
    "Silver",
    "Shadow-matter",
    "Crystal"
]

LOCATIONS = [
    "Vault",
    "Spire",
    "Sanctum",
    "Crypt",
    "Abyss",
    "Labyrinth"
]

TERRAIN_TYPES = [
    "Ashfield", "Rotwood", "Hollow",
    "Wastes", "Fenlands"
]

ZONE_MODIFIERS = [
    "Blighted", "Ancient", "Forsaken",
    "Sunken", "Fractured"
]

class Resource(enum.Enum):
    RAW_AETHER = "raw_aether"
    OBSIDIAN = "obsidian"
    BONE = "bone"
    SHADOW_MATTER = "shadow_matter"
    KNOWLEDGE = "knowledge"


SPECIALIZATIONS = [
    "Prospector",
    "Scholar",
    "Warder"
]

SPECIALIZATION_DESC = {
    "Prospector": "Prospector - gifted at identifying resource hotspots and extracting raw resources from world zones.",
    "Scholar": "Scholar - seeks ancient knowledge as a resource.",
    "Warder": "Warder - skilled combatants whose purpose is battle."
}
