import json
import random
import os

# =========================
# CONSTANTS
# =========================

SAVE_FOLDER = "saves"
MAX_LEVEL = 100

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


# =========================
# HERO CLASS
# =========================

class Hero:
    """A hero that delves into the dungeon depths."""

    def __init__(self, hero_id, name, specialization):
        self.hero_id = hero_id
        self.name = name
        self.specialization = specialization

        # Vital stats — all start at 100
        self.health = 100.0
        self.stamina = 100.0
        self.sanity = 100.0

        # Progression
        self.level = 1
        self.experience = 0

        # Status
        self.current_depth = 0
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
        print(f"  Depth: {self.current_depth}  |  Expeditions: {self.expeditions_completed}")
        print(f"  Status: {'Alive' if self.is_alive else 'Dead'}")
        if self.inventory:
            print(f"  Inventory: {', '.join(f'{k}: {v}' for k, v in self.inventory.items())}")
        else:
            print("  Inventory: (empty)")
        print("-" * 30)

    def take_damage(self, amount):
        """Reduce health, clamped to zero. Kills hero if health reaches zero."""
        self.health = max(0.0, self.health - amount)
        if self.health <= 0:
            self.is_alive = False

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

    return {
        "level_id": level_number,
        "level_name": generate_level_name(),
        "aether_density": calculate_aether_density(level_number),
        "guardian_level": calculate_guardian_power(level_number),
    }


def generate_dungeon_world(max_level=MAX_LEVEL):

    return {
        f"Level {level}": create_level_data(level)
        for level in range(1, max_level + 1)
    }


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

    with open(filepath, "w") as file:
        json.dump(world_data, file, indent=4)

    print(f"--- WORLD '{save_name}' SAVED ---")


def load_dungeon_world(save_name):
    """
    Load a saved dungeon world.
    """

    filepath = get_save_path(save_name)

    try:

        with open(filepath, "r") as file:
            world_data = json.load(file)

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
        f"Level {level_data['level_id']}: "
        f"{level_data['level_name']}"
    )

    print(
        f"  > Aether: "
        f"{level_data['aether_density']} units"
    )

    print(
        f"  > Guardian: "
        f"Pwr Lvl {level_data['guardian_level']}"
    )

    print("-" * 30)


def display_world_overview(world_data):
    """
    Display all dungeon levels.
    """

    print("\n--- THE GREAT DESCENT ---")

    for level_data in world_data.values():
        display_level_summary(level_data)


def display_random_level(world_data):
    """
    Display a random level.
    """

    random_level_number = random.randint(
        1,
        MAX_LEVEL
    )

    level_key = f"Level {random_level_number}"

    level_data = world_data[level_key]

    print(
        f"\n[DISCOVERY] "
        f"{level_key}: "
        f"{level_data['level_name']}"
    )

    print(
        f"Stats: "
        f"Aether {level_data['aether_density']} | "
        f"Guardian {level_data['guardian_level']}"
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
            "The Abyss only goes "
            "to Level 100."
        )

        return

    level_key = f"Level {level_number}"

    level_data = world_data[level_key]

    print(
        f"\n[FOUND] "
        f"{level_data['level_name']}"
    )

    print(
        f"Logic Specs: "
        f"Density {level_data['aether_density']} | "
        f"Power {level_data['guardian_level']}"
    )


# =========================
# ORACLE SYSTEM
# =========================

def process_user_command(
    command,
    world_data,
    heroes
):
    """
    Process oracle commands including hero management.
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

        recruit_hero(heroes)

        return True

    elif cleaned_command == "heroes":

        if not heroes:

            print("No heroes have been recruited yet.")

        else:

            print("\n--- RECRUITED HEROES ---")

            for hero in heroes:

                print(
                    f"  #{hero.hero_id} {hero.name} - "
                    f"Lvl {hero.level} {hero.specialization}"
                )

                print(
                    f"    HP:{hero.health:.0f} "
                    f"ST:{hero.stamina:.0f} "
                    f"SN:{hero.sanity:.0f} "
                    f"| {'Alive' if hero.is_alive else 'Dead'}"
                )

        return True

    elif cleaned_command.startswith("hero "):

        try:

            hero_id = int(
                cleaned_command.split(" ")[1]
            )

            found = None

            for h in heroes:

                if h.hero_id == hero_id:

                    found = h

                    break

            if found:

                found.display_status()

            else:

                print(f"No hero with ID {hero_id}.")

        except (ValueError, IndexError):

            print("Usage: hero <id>")

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


def run_oracle_system(world_data, heroes):
    """
    Main interactive command loop with hero management.
    """

    print("\n--- ORACLE SYSTEM ACTIVE ---")

    print(
        "Options: Type a level number "
        "(1-100), "
        "'random', "
        "'recruit', "
        "'heroes', "
        "'hero <id>', "
        "or 'exit'."
    )

    is_running = True

    while is_running:

        user_command = input(
            "\nEnter Command: "
        )

        is_running = process_user_command(
            user_command,
            world_data,
            heroes
        )


# =========================
# HERO MANAGEMENT
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


# =========================
# MAIN PROGRAM
# =========================

def main():

    dungeon_world, save_name = (
        initialize_world()
    )

    heroes = []

    print(
        f"\n--- ACTIVE WORLD: "
        f"{save_name} ---"
    )

    display_world_overview(
        dungeon_world
    )

    run_oracle_system(
        dungeon_world,
        heroes
    )


if __name__ == "__main__":
    main()