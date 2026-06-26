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
    AETHER_CRYSTALS = "aether_crystals"
    AETHERITE = "aetherite"
    BLOOD = "blood"
    CATTLE = "cattle"
    COPPER = "copper"
    CREATURES = "creatures"
    FIBRE = "fibre"
    FRUITS = "fruits"
    GUARDIAN_CORES = "guardian_cores"
    HARD_ROCK = "hard_rock"
    IRON = "iron"
    KNOWLEDGE = "knowledge"
    LIGHT_METALS = "light_metals"
    LIQUID_AETHER = "liquid_aether"
    MEAT = "meat"
    MEDICINAL_PLANTS = "medicinal_plants"
    RARE_METALS = "rare_metals"
    SEEDS = "seeds"
    SOFT_ROCK = "soft_rock"
    STONE = "stone"
    WATER = "water"
    WOOD = "wood"

#create resource descriptions. For example, wood could be a resource that is used for crafting and construction, and it could be gathered from certain zones or obtained from certain creatures. It could have attributes such as flammability, durability, and flexibility.
RESOURCE_DESCRIPTIONS = {
    Resource.WOOD: "Wood - a versatile material used for crafting and construction, obtained from trees in various zones.",
    Resource.STONE: "Stone - a durable material used for building and infrastructure, found in quarries and caves.",
    Resource.IRON: "Iron - a strong metal used for crafting tools and weapons, mined from underground deposits.",
    # Add more resource descriptions as needed
}

#create categories for resources. For instance renewable resources, where an attribute could exist called is_renewable.

SPECIALIZATIONS = [
    "Prospector",
    "Researcher",
    "Adventurer",
    "Scout",
    "Warrior",
    "Advisor",
]

SPECIALIZATION_DESC = {
    "Prospector": "Prospector - specialise in detecting resource hotspots during expeditions, as well as mining hotspots even within the dungeon. Best for resource extraction expeditions; crucial for turning fruitless expeditions to fruitful ones. Not suited for battle though they can offer such service. Produced by a certain guardian type.",
    "Researcher": "Researcher - Specialise in gathering knowledge in zones during expeditions. Crucial to bringing knowledge back to the dungeon, as well as performing high-level research on the knowledge that is brought back to create recipes for crafting. Best for knowledge-focused expeditions. Produced by a certain guardian type. Not suited for battle.",
    "Warrior": "Warrior - specialise in combat and especially strong against all manner of dungeon enemies from beast and creatures all the way to humans and human-organised attacks. Crucial for safety of expedition parties, and best for expeditions that require killing certain creatures or wiping out certain enemies. They have exceptionally low resource gathering, planning  and logistics capabilities. Full capabilities are drawn under Adventurer types. Produced by a certain guardian type.",
    "Scout": "Scout - best for scouting zones and providing information on potential risks in these zones, as well as rewards. Crucial for long-term planning and zone discovery. Produced by a certain guardian type.",
    "Adventurer": "Adventurer - heroes with excellent planning and logistics skills, who are specialised at leading expeditions and controlling other units during expeditions. They are capable of handling expeditions with hyper-specific goals. They are naturally all-rounders, with a tiny bit of skill in every field. Produced by a specific guardian type.",
    "Advisor": "Advisor - best for providing strategic advice during expeditions, as well as long-term strategic planning. They are not directly involved in expeditions, but their advice can be crucial for the success of expeditions and the management of the dungeon. Produced by a certain guardian type.",

}

INITIAL_SUPPLIES = 50
SUPPLY_COST_PER_TURN = 3
MAX_EXPEDITION_TURNS_PER_TIER: dict[int, int] = {1: 5, 2: 10, 3: 15}
EXPEDITION_COST_RESOURCES = [Resource.WOOD, Resource.FIBRE, Resource.MEAT, Resource.WATER]

HERO_COSTS = {
    "Prospector": {Resource.AETHERITE: 10, Resource.BLOOD: 5},
    "Researcher": {Resource.AETHERITE: 15, Resource.KNOWLEDGE: 10},
    "Warrior": {Resource.AETHERITE: 20, Resource.BLOOD: 15},
    "Scout": {Resource.AETHERITE: 12, Resource.BLOOD: 8},
    "Adventurer": {Resource.AETHERITE: 18, Resource.BLOOD: 12},
    "Advisor": {Resource.AETHERITE: 25, Resource.KNOWLEDGE: 20}
}
