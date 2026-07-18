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

RESOURCE_DESCRIPTIONS={
    Resource.AETHER_CRYSTALS: "Aether crystals : Found exclusively in the dungeon. Aether crystals grow from aether flow\n"
                              "in the dungeon. It can be obtained on every level. It is a consumable resource. Resource nodes\n"
                              "are slowly replenished as ticks pass. It is primarily processed into purer forms like\n"
                              "aetherite and liquid aether for permanent upgrades on unit stats, as well as the creation of units.",
    Resource.WOOD: "Wood : Found exclusively outside the dungeon, within the world zones. Used in building and construction. Also\n"
                   "as an integral resource for expeditions and research tools.",
    Resource.BLOOD: "Blood : Obtained from living creatures up above and fresh carcasses in the dungeon depths. Used for\n"
                    "feeding guardians and creating units.",
    Resource.MEAT: "Meat : Obtained from living creatures up above and fresh carcasses in the dungeon depths. Used for\n"
                   "feeding guardians, creating units and a useful resource for expeditions.",
    Resource.KNOWLEDGE: "Knowledge : Obtained from research and expeditions. Used for creating new recipes and unlocking\n"
                        "new technologies. It is a static resource that is not consumed, but rather accumulated. It is unlocked in pieces,\n"
                        "as in, you can only unlock certain technologies with certain pieces of knowledge.",
    Resource.STONE: "Stone : Can be found in the dungeon and outside the dungeon. Integral for building and construction, as well as feeding some\n"
                    " units. It is a consumable resource.",
    Resource.SOFT_ROCK: "Soft Rock : Can be found in the dungeon and outside the dungeon. Integral for building and construction, as well as feeding some\n"
                        " guardians. It is a consumable resource.",
    Resource.HARD_ROCK: "Hard Rock : Can be found in the dungeon and outside the dungeon. Integral for building and construction, as well as feeding some\n"
                        " guardians. It is a consumable resource.",
    Resource.IRON: "Iron : Can be found in the dungeon and outside the dungeon. Integral for building and construction, as well as feeding some\n"
                    " guardians. It is a consumable resource. It is an integral resource in research tools and better expedition equipment.",
    Resource.COPPER: "Copper : Can be found in the dungeon and outside the dungeon. Integral for research tools.\n"
                    " It is a consumable resource.",
    Resource.AETHERITE: "Aetherite : Found exclusively in the dungeon. Aetherite is a purer form of aether crystals, and is used for permanent upgrades on unit stats\n"
                    " as well as the creation of units. It is a consumable resource.",
    #will add more resource descriptions later
}
class ResourceCategory(enum.Enum):
    CONSUMABLE = "consumable"
    STATIC = "static"


RESOURCE_CATEGORIES: dict[Resource, ResourceCategory] = {
    Resource.KNOWLEDGE: ResourceCategory.STATIC,
}

CONSUMABLE_RESOURCES: list[Resource] = [
    r for r in Resource
    if RESOURCE_CATEGORIES.get(r, ResourceCategory.CONSUMABLE)
    == ResourceCategory.CONSUMABLE
]

INITIAL_STOCKPILE: dict[Resource, int] = {
    Resource.BLOOD: 7,
    Resource.WATER: 3,
    Resource.STONE: 5,
    Resource.AETHER_CRYSTALS: 15,
    Resource.WOOD: 3,
}

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
#Expeditions should be free for a set number of successful ones; maybe 5 or 6 or something.
#Like how players get free DNA in Plague Inc. at the beginning of the game. Costs don't scale significantly until mid-game.

GUARDIAN_BLOOD_COST = 1
#Guardian blood costs should set in after the set number of times mentioned in the comment above.

HERO_COSTS = {"Base Hero Cost": {Resource.AETHER_CRYSTALS: 5, Resource.WATER: 3, Resource.BLOOD: 2,  Resource.WOOD: 3},
              #The base hero cost is the cost without specializations, mentioned in GAME_DETAILS_AND_PLANNING.md
              #I'm thinking of further defining specialised hero costs, to make things clearer.
    "Prospector": {Resource.AETHERITE: 10, Resource.BLOOD: 5},
    "Researcher": {Resource.AETHERITE: 15, Resource.KNOWLEDGE: 10},
    "Warrior": {Resource.AETHERITE: 20, Resource.BLOOD: 15},
    "Scout": {Resource.AETHERITE: 12, Resource.BLOOD: 8},
    "Adventurer": {Resource.AETHERITE: 18, Resource.BLOOD: 12},
    "Advisor": {Resource.AETHERITE: 25, Resource.KNOWLEDGE: 20}
}

WARDER_COST = {Resource.BLOOD: 1, Resource.AETHER_CRYSTALS: 1}
#Five of them can be created initially.

BUILDER_COST = {Resource.STONE: 1, Resource.AETHER_CRYSTALS: 1}
#Five of them can be created initially.