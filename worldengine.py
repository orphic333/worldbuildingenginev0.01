import json
import random
import os

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


# =========================
# UNIT BASE CLASS
# =========================

class BaseUnit:
    """Base class for all units in the game."""

    def __init__(self, unit_id, name, health=100.0):
        self.unit_id = unit_id
        self.name = name
        self.health = health
        self.is_alive = True

    def take_damage(self, amount):
        """Reduce health, clamped to zero. Kills unit if health reaches zero."""
        self.health = max(0.0, self.health - amount)
        if self.health <= 0:
            self.is_alive = False


# =========================
# HERO CLASS
# =========================

class Hero(BaseUnit):
    """A hero that delves into the dungeon depths."""

    def __init__(self, hero_id, name, specialization):
        super().__init__(hero_id, name)
        self.specialization = specialization

        # Vital stats
        self.stamina = 100.0
        self.sanity = 100.0

        # Progression
        self.level = 1
        self.experience = 0

        # Status
        self.current_zone = None
        self.is_alive = True

        # Inventory / history
        self.inventory = {}
        self.expeditions_completed = 0

    def display_status(self):
        """Print formatted hero stats."""
        print(f"\n=== {self.name} ===")
        print(f"  Specialization: {self.specialization}")
        print(f"  Level: {self.level}  |  XP: {self.experience}")
        print(f"  Health: {self.health:.1f}  |  Stamina: {self.stamina:.1f}  |  Sanity: {self.sanity:.1f}")
        print(f"  Zone: {self.current_zone}  |  Expeditions: {self.expeditions_completed}")
        print(f"  Status: {'Alive' if self.is_alive else 'Dead'}")
        if self.inventory:
            print(f"  Inventory: {', '.join(f'{k}: {v}' for k, v in self.inventory.items())}")
        else:
            print("  Inventory: (empty)")
        print("-" * 30)

    def lose_sanity(self, amount):
        """Reduce sanity, clamped to zero."""
        self.sanity = max(0.0, self.sanity - amount)

    def consume_stamina(self, amount):
        """Reduce stamina, clamped to zero."""
        self.stamina = max(0.0, self.stamina - amount)

    def gain_experience(self, amount):
        """Add XP and level up every threshold."""
        self.experience += amount
        while self.experience >= self.level * 100:
            self.experience -= self.level * 100
            self.level += 1
            print(f"  *** {self.name} reached level {self.level}! ***")

    def add_resource(self, resource_name, amount):
        """Add a resource to the hero's inventory."""
        self.inventory[resource_name] = self.inventory.get(resource_name, 0) + amount


# =========================
# GUARDIAN AND BUILDER CLASSES
# =========================

class Guardian(BaseUnit):
    """A guardian assigned to protect dungeon levels."""

    def __init__(self, guardian_id, name, power=10.0):
        super().__init__(guardian_id, name)
        self.assigned_level_id = None
        self.power = power

    def display_status(self):
        """Print formatted guardian stats."""
        print(f"\n=== {self.name} ===")
        print(f"  ID: {self.unit_id}")
        print(f"  Power: {self.power}")
        print(f"  Assigned Level: {self.assigned_level_id}")
        print(f"  Health: {self.health:.1f}")
        print(f"  Status: {'Alive' if self.is_alive else 'Dead'}")
        print("-" * 30)


class Builder(BaseUnit):
    """A builder that constructs and upgrades dungeon structures."""

    def __init__(self, builder_id, name, build_speed=1.0):
        super().__init__(builder_id, name)
        self.build_speed = build_speed
        self.current_task = None

    def display_status(self):
        """Print formatted builder stats."""
        print(f"\n=== {self.name} ===")
        print(f"  ID: {self.unit_id}")
        print(f"  Build Speed: {self.build_speed}")
        print(f"  Current Task: {self.current_task}")
        print(f"  Health: {self.health:.1f}")
        print(f"  Status: {'Alive' if self.is_alive else 'Dead'}")
        print("-" * 30)


# =========================
# CORE CALCULATIONS
# =========================

def calculate_aether_density(level):

    density = 1.8 * level**2 + 2 * level + 16

    return round(density, 3)


def calculate_guardian_power(level):

    return round(level * 1.1, 3)


# =========================
# DUNGEON DATA CLASSES
# =========================

class DungeonLevel:
    """A single level within the dungeon."""

    def __init__(self, level_id, name, aether_density, guardian_power,
                 resource_nodes=None, structural_mods=None,
                 active_events=None, is_explored=False):
        self.level_id = level_id
        self.name = name
        self.aether_density = aether_density
        self.guardian_power = guardian_power
        self.resource_nodes = resource_nodes if resource_nodes is not None else {}
        self.structural_mods = structural_mods if structural_mods is not None else []
        self.active_events = active_events if active_events is not None else []
        self.is_explored = is_explored

    def to_dict(self):
        """Serialize level to a JSON-safe dict."""
        return {
            "level_id": self.level_id,
            "name": self.name,
            "aether_density": self.aether_density,
            "guardian_power": self.guardian_power,
            "resource_nodes": self.resource_nodes,
            "structural_mods": self.structural_mods,
            "active_events": self.active_events,
            "is_explored": self.is_explored,
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize a level from a dict."""
        return cls(
            level_id=data["level_id"],
            name=data["name"],
            aether_density=data["aether_density"],
            guardian_power=data["guardian_power"],
            resource_nodes=data.get("resource_nodes", {}),
            structural_mods=data.get("structural_mods", []),
            active_events=data.get("active_events", []),
            is_explored=data.get("is_explored", False),
        )


class WorldZone:
    """A zone within the outside world surrounding the dungeon."""

    def __init__(self, zone_id, name, tier, danger_rating,
                 resource_nodes=None, is_discovered=False,
                 threat_level=0):
        self.zone_id = zone_id
        self.name = name
        self.tier = tier
        self.danger_rating = danger_rating
        self.resource_nodes = resource_nodes if resource_nodes is not None else {}
        self.is_discovered = is_discovered
        self.threat_level = threat_level

    def to_dict(self):
        """Serialize zone to a JSON-safe dict."""
        return {
            "zone_id": self.zone_id,
            "name": self.name,
            "tier": self.tier,
            "danger_rating": self.danger_rating,
            "resource_nodes": self.resource_nodes,
            "is_discovered": self.is_discovered,
            "threat_level": self.threat_level,
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize a zone from a dict."""
        return cls(
            zone_id=data["zone_id"],
            name=data["name"],
            tier=data["tier"],
            danger_rating=data["danger_rating"],
            resource_nodes=data.get("resource_nodes", {}),
            is_discovered=data.get("is_discovered", False),
            threat_level=data.get("threat_level", 0),
        )


class DungeonWorld:
    """A named dungeon world containing multiple levels and zones."""

    def __init__(self, name="", levels=None, turn=0,
                 zones=None, known_zones=None):
        self.name = name
        self.levels = levels if levels is not None else {}
        self.turn = turn
        self.zones = zones if zones is not None else {}
        self.known_zones = known_zones if known_zones is not None else []

    def to_dict(self):
        """Serialize world to a JSON-safe dict."""
        return {
            "name": self.name,
            "turn": self.turn,
            "levels": {
                str(lvl_id): level.to_dict()
                for lvl_id, level in self.levels.items()
            },
            "zones": {
                str(zone_id): zone.to_dict()
                for zone_id, zone in self.zones.items()
            },
            "known_zones": self.known_zones,
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize a world from a dict."""
        name = data.get("name", "")
        turn = data.get("turn", 0)
        levels = {}
        for lvl_id_str, level_data in data.get("levels", {}).items():
            level = DungeonLevel.from_dict(level_data)
            levels[level.level_id] = level
        zones = {}
        for zone_id_str, zone_data in data.get("zones", {}).items():
            zone = WorldZone.from_dict(zone_data)
            zones[zone.zone_id] = zone
        known_zones = data.get("known_zones", [])
        return cls(name=name, levels=levels, turn=turn,
                   zones=zones, known_zones=known_zones)


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


# =========================
# SAVE SYSTEM
# =========================

def ensure_save_directory_exists():
    """
    Create save folder if missing.
    """

    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)


def get_save_path(save_name):
    """
    Build full save filepath.
    """

    return os.path.join(
        SAVE_FOLDER,
        f"{save_name}.json"
    )


def list_save_files():
    """
    Return all available save names.
    """

    ensure_save_directory_exists()

    save_files = os.listdir(SAVE_FOLDER)

    return [
        file.replace(".json", "")
        for file in save_files
        if file.endswith(".json")
    ]


def save_dungeon_world(world_data, save_name):
    """
    Save world data to JSON.
    """

    filepath = get_save_path(save_name)

    world_data.name = save_name

    with open(filepath, "w") as file:
        json.dump(world_data.to_dict(), file, indent=4)

    print(f"--- WORLD '{save_name}' SAVED ---")


def load_dungeon_world(save_name):
    """
    Load a saved dungeon world.
    """

    filepath = get_save_path(save_name)

    try:

        with open(filepath, "r") as file:
            data = json.load(file)

        # Backward compat: pre-refactor saves use flat "Level N" keys
        if isinstance(data, dict) and any(
            k.startswith("Level ") for k in data
        ):

            levels = {}

            for key, level_data in data.items():

                levels[level_data["level_id"]] = DungeonLevel(
                    level_id=level_data["level_id"],
                    name=level_data["level_name"],
                    aether_density=level_data["aether_density"],
                    guardian_power=level_data["guardian_level"],
                )

            world_data = DungeonWorld(levels=levels)

        else:

            world_data = DungeonWorld.from_dict(data)

        print(f"--- WORLD '{save_name}' LOADED ---")

        return world_data

    except FileNotFoundError:

        return None


# =========================
# WORLD INITIALIZATION
# =========================

def display_save_files(save_files):
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


def create_new_world():
    """
    Create and save a new dungeon world.
    """

    save_name = input(
        "\nEnter new world name: "
    ).strip()

    if not save_name:

        print("Invalid world name.")

        return create_new_world()

    dungeon_world = generate_dungeon_world()

    save_dungeon_world(
        dungeon_world,
        save_name
    )

    print("--- NEW WORLD GENERATED ---")

    return dungeon_world, save_name


def select_existing_world(save_files):
    """
    Load a selected save file.
    """

    try:

        selection = int(
            input("\nSelect save number: ")
        )

        selected_save = save_files[
            selection - 1
        ]

        dungeon_world = load_dungeon_world(
            selected_save
        )

        return dungeon_world, selected_save

    except (
        ValueError,
        IndexError
    ):

        print("Invalid selection.")

        return select_existing_world(
            save_files
        )


def initialize_world():
    """
    Handle startup world selection.
    """

    save_files = list_save_files()

    display_save_files(save_files)

    print("\nOptions:")
    print("1. Load Existing World")
    print("2. Create New World")

    choice = input(
        "\nEnter choice: "
    ).strip()

    if choice == "1":

        if not save_files:

            print("No saves available.")

            return create_new_world()

        return select_existing_world(
            save_files
        )

    elif choice == "2":

        return create_new_world()

    else:

        print("Invalid option.")

        return initialize_world()


# =========================
# DISPLAY HELPERS
# =========================

def display_level_summary(level_data):
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
        f"Pwr Lvl {level_data.guardian_power}"
    )

    print("-" * 30)


def display_world_overview(world_data):
    """
    Display all dungeon levels.
    """

    print("\n--- THE GREAT DESCENT ---")

    for level_data in world_data.levels.values():
        display_level_summary(level_data)


def display_random_level(world_data):
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
        f"Guardian {level_data.guardian_power}"
    )


def display_specific_level(
    world_data,
    level_number
):
    """
    Display chosen level data.
    """

    if not 1 <= level_number <= MAX_LEVEL:

        print(
            f"The Abyss only goes "
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
        f"Power {level_data.guardian_power}"
    )


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


# =========================
# UNIT MANAGEMENT
# =========================

SPECIALIZATIONS = [
    "Prospector",
    "Scholar",
    "Warder"
]

SPECIALIZATION_DESC = {
    "Prospector": "Prospector - gifted at extracting raw resources from the depths.",
    "Scholar": "Scholar - seeks ancient knowledge hidden in the dark.",
    "Warder": "Warder - built to endure the dangers of the deep."
}


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


def recruit_guardian(guardians):
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
    ).strip()

    if not name:

        print("A builder must have a name.")

        return recruit_builder(builders)

    builder = Builder(builder_id, name)

    builders.append(builder)

    print(
        f"\n--- {name} the Builder has arrived! ---"
    )

    return builder


# =========================
# MAIN PROGRAM
# =========================

def main():

    dungeon_world, save_name = (
        initialize_world()
    )

    heroes = []
    guardians = []
    builders = []

    print(
        f"\n--- ACTIVE WORLD: "
        f"{save_name} ---"
    )

    display_world_overview(
        dungeon_world
    )

    run_oracle_system(
        dungeon_world,
        heroes,
        guardians,
        builders
    )


if __name__ == "__main__":
    main()