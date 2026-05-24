from .constants import Resource


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
    """A hero that engages in expeditions to explore the world."""

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
# EXPEDITION CLASS
# =========================

class Expedition:
    """Represents a hero expedition into a zone."""

    def __init__(self, hero, target_zone, world,
                 duration_turns, turns_elapsed=0,
                 status="active", loot=None):
        self.hero = hero
        self.target_zone = target_zone
        self.world = world
        self.duration_turns = duration_turns
        self.turns_elapsed = turns_elapsed
        self.status = status
        self.loot = loot if loot is not None else {}

    def advance(self):
        """Advance this expedition by one turn."""

        self.turns_elapsed += 1

        self._apply_zone_pressure()

        if self.turns_elapsed >= self.duration_turns:

            self._resolve()

    def _apply_zone_pressure(self):
        """Apply environmental damage from the zone."""

        self.hero.consume_stamina(
            self.target_zone.danger_rating * 0.4
        )

        self.hero.lose_sanity(
            self.target_zone.tier * 2.0
        )

        self.hero.take_damage(
            self.target_zone.danger_rating * 0.2
        )

        if not self.hero.is_alive:

            self.status = "failed"

    def _resolve(self):
        """Finalise the expedition and award rewards."""

        self.loot = {}

        for resource, node_value in (
            self.target_zone.resource_nodes.items()
        ):

            if node_value <= 0:

                continue

            harvest = min(
                node_value,
                int(node_value * 0.3) + 1
            )

            if (
                resource == Resource.KNOWLEDGE
                and self.hero.specialization == "Scholar"
            ):

                harvest *= 2

            self.target_zone.resource_nodes[resource] = (
                max(
                    0,
                    self.target_zone.resource_nodes[resource]
                    - harvest
                )
            )

            self.loot[resource] = harvest

        xp_gain = int(
            self.target_zone.danger_rating
            * self.target_zone.tier
            * 5
        )

        self.hero.gain_experience(xp_gain)

        if not self.target_zone.is_discovered:

            self.target_zone.is_discovered = True

            self.world.known_zones.append(
                self.target_zone.zone_id
            )

            print(
                f"\n  [DISCOVERED] {self.target_zone.name} "
                f"(Tier {self.target_zone.tier})!"
            )

        self.hero.current_zone = None

        self.status = "returned"

        print(
            f"\n  [RETURN] {self.hero.name} returned from "
            f"{self.target_zone.name} "
            f"(Tier {self.target_zone.tier})."
        )

        print(
            f"    Loot: {self.loot} "
            f"| XP: {xp_gain}"
        )

        print(
            f"    HP:{self.hero.health:.0f} "
            f"ST:{self.hero.stamina:.0f} "
            f"SN:{self.hero.sanity:.0f}"
        )


# =========================
# DUNGEON DATA CLASSES
# =========================

class DungeonLevel:
    """A single level within the dungeon."""

    def __init__(self, level_id, name, aether_density, guardian_power_level,
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
            "resource_nodes": {
                r.value: qty
                for r, qty in self.resource_nodes.items()
            },
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
            resource_nodes={
                Resource(k): v
                for k, v
                in data.get("resource_nodes", {}).items()
            },
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
            "resource_nodes": {
                r.value: qty
                for r, qty in self.resource_nodes.items()
            },
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
            resource_nodes={
                Resource(k): v
                for k, v
                in data.get("resource_nodes", {}).items()
            },
            is_discovered=data.get("is_discovered", False),
            threat_level=data.get("threat_level", 0),
        )


class DungeonWorld:
    """A named dungeon world containing multiple levels and zones."""

    def __init__(self, name="", levels=None, turn=0,
                 zones=None, known_zones=None,
                 active_expeditions=None,
                 stockpile=None):
        self.name = name
        self.levels = levels if levels is not None else {}
        self.turn = turn
        self.zones = zones if zones is not None else {}
        self.known_zones = known_zones if known_zones is not None else []
        self.active_expeditions = (
            active_expeditions
            if active_expeditions is not None
            else []
        )
        self.stockpile = (
            stockpile
            if stockpile is not None
            else {r: 0 for r in Resource}
        )

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
            "active_expeditions": [
                {
                    "hero_id": exp.hero.unit_id,
                    "target_zone_id": (
                        exp.target_zone.zone_id
                    ),
                    "duration_turns": (
                        exp.duration_turns
                    ),
                    "turns_elapsed": (
                        exp.turns_elapsed
                    ),
                    "status": exp.status,
                    "loot": {
                        r.value: qty
                        for r, qty in exp.loot.items()
                    },
                }
                for exp in self.active_expeditions
            ],
            "stockpile": {
                r.value: qty
                for r, qty in self.stockpile.items()
            },
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

        raw_stockpile = data.get("stockpile")

        if raw_stockpile:

            stockpile = {
                Resource(k): v
                for k, v in raw_stockpile.items()
            }

        else:

            stockpile = {r: 0 for r in Resource}

        return cls(name=name, levels=levels, turn=turn,
                   zones=zones, known_zones=known_zones,
                   stockpile=stockpile)

    def tick(self, heroes, guardians, builders):
        """Advance the game by one turn."""

        self.turn += 1

        self._process_expeditions(heroes)

        self._process_environmental_events(
            heroes, guardians
        )

        self._process_unit_statuses(
            heroes, guardians, builders
        )

        print(f"\n--- Turn {self.turn} ---")

    def _process_expeditions(self, heroes):
        """Advance all active expeditions, removing completed or failed ones."""

        completed = []

        for exp in self.active_expeditions:

            exp.advance()

            if exp.status in ("returned", "failed"):

                completed.append(exp)

                if exp.status == "returned":

                    for resource, qty in exp.loot.items():

                        self.stockpile[resource] += qty

                        print(
                            f"    [DEPOSIT] "
                            f"{resource.value}: +{qty}"
                        )

                if exp.status == "failed":

                    print(
                        f"\n  [FAILURE] {exp.hero.name} "
                        f"perished in {exp.target_zone.name}!"
                    )

        for exp in completed:

            self.active_expeditions.remove(exp)

    def _process_environmental_events(
        self, heroes, guardians
    ):
        """Stub: process hazards and events."""

        print(
            "  [Tick] Environmental events phase "
            "(not yet implemented)"
        )

    def _process_unit_statuses(
        self, heroes, guardians, builders
    ):
        """Stub: update unit vitals and cooldowns."""

        print(
            "  [Tick] Unit status phase "
            "(not yet implemented)"
        )
