import json
import random

# =========================
# CONSTANTS
# =========================

WORLD_FILE = "world_data.json"
MAX_LEVEL = 200

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
# CORE CALCULATIONS
# =========================

def calculate_aether_density(level):
    """
    Calculate aether density for a dungeon level.
    """
    density = 1.8 * level**2 + 2 * level + 16
    return round(density, 3)


def calculate_guardian_power(level):
    """
    Calculate guardian power scaling.
    """
    return round(level * 1.1, 3)


# =========================
# LEVEL GENERATION
# =========================

def generate_level_name():
    """
    Generate a procedural dungeon level name.
    """
    adjective = random.choice(ADJECTIVES)
    material = random.choice(MATERIALS)
    location = random.choice(LOCATIONS)

    return f"The {adjective} {material} {location}"


def create_level_data(level_number):
    """
    Create all data for a single dungeon level.
    """
    return {
        "level_id": level_number,
        "level_name": generate_level_name(),
        "aether_density": calculate_aether_density(level_number),
        "guardian_level": calculate_guardian_power(level_number),
    }


def generate_dungeon_world(max_level=MAX_LEVEL):
    """
    Generate the entire dungeon world.
    """
    return {
        f"Level {level}": create_level_data(level)
        for level in range(1, max_level + 1)
    }


# =========================
# FILE MANAGEMENT
# =========================

def save_dungeon_world(world_data, filename=WORLD_FILE):
    """
    Save dungeon data to JSON file.
    """
    with open(filename, "w") as file:
        json.dump(world_data, file, indent=4)

    print("--- WORLD SAVED TO VAULT ---")


def load_dungeon_world(filename=WORLD_FILE):
    """
    Load dungeon data from JSON file.
    """
    try:
        with open(filename, "r") as file:
            world_data = json.load(file)

        print("--- WORLD DATA RECOVERED ---")
        return world_data

    except FileNotFoundError:
        print("No save file found.")
        return None


def initialize_world():
    """
    Load existing world or generate a new one.
    """
    existing_world = load_dungeon_world()

    if existing_world is not None:
        return existing_world

    new_world = generate_dungeon_world()
    save_dungeon_world(new_world)

    print("--- NEW WORLD GENERATED ---")

    return new_world


# =========================
# DISPLAY HELPERS
# =========================

def display_level_summary(level_data):
    """
    Print formatted level information.
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
    Print all dungeon levels.
    """
    print("--- THE GREAT DESCENT ---")

    for level_data in world_data.values():
        display_level_summary(level_data)


def display_random_level(world_data):
    """
    Display a random dungeon level.
    """
    random_level_number = random.randint(1, MAX_LEVEL)

    level_key = f"Level {random_level_number}"
    level_data = world_data[level_key]

    print(
        f"\n[DISCOVERY] "
        f"{level_key}: {level_data['level_name']}"
    )

    print(
        f"Stats: "
        f"Aether {level_data['aether_density']} | "
        f"Guardian {level_data['guardian_level']}"
    )


def display_specific_level(world_data, level_number):
    """
    Display information for a chosen level.
    """
    if not 1 <= level_number <= MAX_LEVEL:
        print("The Abyss only goes to Level 100.")
        return

    level_key = f"Level {level_number}"
    level_data = world_data[level_key]

    print(f"\n[FOUND] {level_data['level_name']}")

    print(
        f"Logic Specs: "
        f"Density {level_data['aether_density']} | "
        f"Power {level_data['guardian_level']}"
    )


# =========================
# USER INPUT
# =========================

def process_user_command(command, world_data):
    """
    Process oracle system commands.
    """
    cleaned_command = command.lower().strip()

    if cleaned_command == "exit":
        print("Closing the Vault. Goodbye, Architect.")
        return False

    if cleaned_command == "random":
        display_random_level(world_data)
        return True

    if cleaned_command.isdigit():
        level_number = int(cleaned_command)
        display_specific_level(world_data, level_number)
        return True

    print("The Oracle does not understand.")
    return True


def run_oracle_system(world_data):
    """
    Main interactive oracle loop.
    """
    print("\n--- ORACLE SYSTEM ACTIVE ---")

    print(
        "Options: Type a level number (1-100), "
        "'random' for a surprise, or 'exit' to quit."
    )

    is_running = True

    while is_running:
        user_command = input("\nEnter Command: ")
        is_running = process_user_command(
            user_command,
            world_data
        )


# =========================
# MAIN PROGRAM
# =========================

def main():
    dungeon_world = initialize_world()

    display_world_overview(dungeon_world)

    run_oracle_system(dungeon_world)


if __name__ == "__main__":
    main()