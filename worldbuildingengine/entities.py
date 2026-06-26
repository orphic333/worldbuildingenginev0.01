from __future__ import annotations

import math
import random

from .constants import (
    Resource, SUPPLY_COST_PER_TURN, MAX_EXPEDITION_TURNS_PER_TIER,
    EXPEDITION_COST_RESOURCES,
)


# =========================
# UNIT BASE CLASS
# =========================

class BaseUnit:
    """Base class for all units in the game."""

    def __init__(self, unit_id: int, name: str | None = None, health: float = 100.0) -> None:
        self.unit_id = unit_id
        if name is not None:
            self.name = name
        self.health = health
        self.is_alive = True

    def take_damage(self, amount: float) -> None:
        """Reduce health, clamped to zero. Kills unit if health reaches zero."""
        self.health = max(0.0, self.health - amount)
        if self.health <= 0:
            self.is_alive = False

    def apply_tick_effects(self) -> None:
        """Apply per-tick effects. Override in subclasses."""
        pass


# =========================
# HERO CLASS
# =========================

class Hero(BaseUnit):
    """A hero that engages in expeditions to explore the world."""

    def __init__(self, hero_id: int, name: str, specialization: str) -> None:
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

    @property
    def is_busy(self):
        return self.current_zone is not None

    def display_status(self) -> None:
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

    def lose_sanity(self, amount: float) -> None:
        """Reduce sanity, clamped to zero."""
        self.sanity = max(0.0, self.sanity - amount)

    def consume_stamina(self, amount: float) -> None:
        """Reduce stamina, clamped to zero."""
        self.stamina = max(0.0, self.stamina - amount)

    def gain_experience(self, amount: int) -> None:
        """Add XP and level up every threshold."""
        self.experience += amount
        while self.experience >= self.level * 100:
            self.experience -= self.level * 100
            self.level += 1
            print(f"  *** {self.name} reached level {self.level}! ***")

    def add_resource(self, resource_name: str, amount: int) -> None:
        """Add a resource to the hero's inventory."""
        self.inventory[resource_name] = self.inventory.get(resource_name, 0) + amount
        #a maximum number of resources should be implemented, and should differ due to hero specialisations.
        #an implementation measure may be a bag.
        #increasing the level of the hero should increase the hero's use of space, and also increase the 'size' of the bag

    def to_dict(self) -> dict:      #hero data serialisation
        return {
            "unit_id": self.unit_id,
            "name": self.name,
            "health": self.health,
            "is_alive": self.is_alive,
            "specialization": self.specialization,
            "stamina": self.stamina,
            "sanity": self.sanity,
            "level": self.level,
            "experience": self.experience,
            "current_zone": self.current_zone,
            "inventory": {
                (r.value if isinstance(r, Resource) else r): qty
                for r, qty in self.inventory.items()
            },
            "expeditions_completed": self.expeditions_completed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Hero:
        hero = cls(
            hero_id=data["unit_id"],
            name=data["name"],
            specialization=data["specialization"]
        )
        hero.health = data["health"]
        hero.is_alive = data["is_alive"]
        hero.stamina = data["stamina"]
        hero.sanity = data["sanity"]
        hero.level = data["level"]
        hero.experience = data["experience"]
        hero.current_zone = data.get("current_zone")
        hero.inventory = {}
        for k, v in data.get("inventory", {}).items():
            try:
                hero.inventory[Resource(k)] = v
            except ValueError:
                hero.inventory[k] = v
        hero.expeditions_completed = data["expeditions_completed"]
        return hero


# =========================
# GUARDIAN AND BUILDER CLASSES
# =========================

class Guardian(BaseUnit):
    """A guardian assigned to protect dungeon levels."""

    def __init__(
        self,
        guardian_id: int,
        name: str,
        level: int = 1,
        recruitment_type: str = "Standard",
        maintenance_costs: dict | None = None,
    ) -> None:
        super().__init__(guardian_id, name)
        self.assigned_level_id = None
        self.level = max(1, level)
        self.recruitment_type = recruitment_type
        self.maintenance_costs = maintenance_costs if maintenance_costs is not None else {}

    @property
    def power_level(self) -> float:
        return float(self.level * 10.0)

    def display_status(self) -> None:
        """Print formatted guardian stats."""
        print(f"\n=== {self.name} ===")
        print(f"  ID: {self.unit_id}")
        print(f"  Level: {self.level}")
        print(f"  Power: {self.power_level}")
        print(f"  Recruitment Type: {self.recruitment_type}")
        if self.maintenance_costs:
            print(
                "  Maintenance: "
                + ", ".join(
                    f"{(r.value if isinstance(r, Resource) else r)}: {qty}"
                    for r, qty in self.maintenance_costs.items()
                )
            )
        else:
            print("  Maintenance: None")
        print(f"  Assigned Level: {self.assigned_level_id}")
        print(f"  Health: {self.health:.1f}")
        print(f"  Status: {'Alive' if self.is_alive else 'Dead'}")
        print("-" * 30)

    def to_dict(self):
        return {
            "unit_id": self.unit_id,
            "name": self.name,
            "health": self.health,
            "is_alive": self.is_alive,
            "assigned_level_id": self.assigned_level_id,
            "level": self.level,
            "power_level": self.power_level,
            "recruitment_type": self.recruitment_type,
            "maintenance_costs": {
                (r.value if isinstance(r, Resource) else r): qty
                for r, qty in self.maintenance_costs.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> Guardian:
        level = data.get("level")
        if level is None:
            power_level = data.get("power_level", 10.0)
            level = max(1, int(round(power_level / 10.0)))

        maintenance_costs = {}
        for k, v in data.get("maintenance_costs", {}).items():
            try:
                maintenance_costs[Resource(k)] = v
            except ValueError:
                maintenance_costs[k] = v

        g = cls(
            guardian_id=data["unit_id"],
            name=data["name"],
            level=level,
            recruitment_type=data.get("recruitment_type", "Standard"),
            maintenance_costs=maintenance_costs,
        )
        g.health = data["health"]
        g.is_alive = data["is_alive"]
        g.assigned_level_id = data.get("assigned_level_id")
        return g


class Builder(BaseUnit):
    """A builder that constructs and upgrades dungeon structures."""

    LIFESPAN_TICK_INTERVAL = 2

    def __init__(self, builder_id: int, build_speed: float = 1.0, name: str = "") -> None:
        super().__init__(builder_id)
        self.build_speed = build_speed
        self.current_task = None
        self.lifespan = 100
        self._tick_counter = 0

    def apply_tick_effects(self) -> None:
        """Reduce lifespan by 1 every 2 ticks. Mark dead when lifespan expires."""
        if not self.is_alive:
            return
        self._tick_counter += 1
        if self._tick_counter >= self.LIFESPAN_TICK_INTERVAL:
            self._tick_counter = 0
            self.lifespan -= 1
            if self.lifespan <= 0:
                self.is_alive = False
                print(f"  [DECAY] Builder #{self.unit_id} has expired.")

    def display_status(self) -> None:
        """Print formatted builder stats."""
        print(f"\n=== Builder #{self.unit_id} ===")
        print(f"  Build Speed: {self.build_speed}")
        print(f"  Current Task: {self.current_task}")
        print(f"  Health: {self.health:.1f}")
        print(f"  Lifespan: {self.lifespan}")
        print(f"  Status: {'Alive' if self.is_alive else 'Dead'}")
        print("-" * 30)

    def to_dict(self):
        return {
            "unit_id": self.unit_id,
            "health": self.health,
            "is_alive": self.is_alive,
            "build_speed": self.build_speed,
            "current_task": self.current_task,
            "lifespan": self.lifespan,
            "_tick_counter": self._tick_counter,
        }

    @classmethod
    def from_dict(cls, data):
        b = cls(
            builder_id=data["unit_id"],
            build_speed=data.get("build_speed", 1.0)
        )
        b.health = data["health"]
        b.is_alive = data["is_alive"]
        b.current_task = data.get("current_task")
        b.lifespan = data.get("lifespan", 100)
        b._tick_counter = data.get("_tick_counter", 0)
        return b

#add advisor class. These ones are more advanced in terms of function
# =========================
# EXPEDITION CLASS
# =========================

class Expedition:
    """Represents a hero expedition into a zone."""

    def __init__(self, hero: Hero, target_zone: WorldZone, world: DungeonWorld,
                 duration_turns: int, turns_elapsed: int = 0,
                 status: str = "active", loot: dict | None = None,
                 has_engaged_event_creature: bool = False,
                 creature_defeated: bool = False) -> None:
        self.hero = hero
        self.target_zone = target_zone
        self.world = world
        self.duration_turns = duration_turns
        self.turns_elapsed = turns_elapsed
        self.status = status
        self.loot = loot if loot is not None else {}
        self.has_engaged_event_creature = has_engaged_event_creature
        self.creature_defeated = creature_defeated

    def advance(self) -> None:
        """Advance this expedition by one turn."""

        if self.status != "active":
            return

        self.turns_elapsed += 1

        if self.status != "active":
            return

        self._apply_zone_pressure()

        if self.status == "active" and self.turns_elapsed >= self.duration_turns:
            self._resolve()

    def _apply_zone_pressure(self) -> None:
        """Apply escalating jittered damage from the zone."""

        escalation = 1 + math.log(1 + self.turns_elapsed)
        jitter = lambda: random.uniform(0.8, 1.2)

        self.hero.consume_stamina(
            self.target_zone.danger_rating * 0.4 * escalation * jitter()
        )

        self.hero.lose_sanity(
            self.target_zone.tier * 2.0 * escalation * jitter()
        )

        self.hero.take_damage(
            self.target_zone.danger_rating * 0.2 * escalation * jitter()
        )

        if self.target_zone.event_creature_active:
            self.hero.lose_sanity(
                self.target_zone.tier * 1.5 * escalation * jitter()
            )
            self.hero.take_damage(
                self.target_zone.event_creature_attack * 0.25 * escalation * jitter()
            )

        if not self.hero.is_alive:
            self.hero.current_zone = None
            self.status = "failed"

    def _resolve_event_creature_encounter(self) -> None:
        """Resolve the rare event creature encounter for this expedition."""

        self.has_engaged_event_creature = True

        zone = self.target_zone
        if not zone.event_creature_active:
            return

        hero_power = (
            self.hero.level * 8.0
            + self.hero.health * 0.5
            + self.hero.stamina * 0.3
        )
        creature_power = (
            zone.event_creature_health * 0.6
            + zone.event_creature_attack * 4.0
        )
        encounter_chance = hero_power / max(1.0, hero_power + creature_power)
        encounter_chance = min(max(encounter_chance, 0.1), 0.9)

        print(
            f"\n  [EVENT] {self.hero.name} encounters "
            f"{zone.event_creature_name}!"
        )

        if random.random() <= encounter_chance:
            creature_damage = max(
                1.0,
                hero_power * random.uniform(0.25, 0.45)
            )
            zone.event_creature_health = max(
                0.0,
                zone.event_creature_health - creature_damage
            )
            self.hero.take_damage(
                zone.event_creature_attack * random.uniform(0.8, 1.2)
            )
            self.hero.lose_sanity(zone.tier * 2.5)
            print(
                f"    [STRIKE] {self.hero.name} wounds "
                f"{zone.event_creature_name} for {creature_damage:.1f} damage."
            )
        else:
            hero_damage = max(
                1.0,
                zone.event_creature_attack * random.uniform(1.0, 1.6)
            )
            self.hero.take_damage(hero_damage)
            self.hero.lose_sanity(zone.tier * 3.5)
            print(
                f"    [BACKLASH] {zone.event_creature_name} lashes out "
                f"for {hero_damage:.1f} damage."
            )

        if not self.hero.is_alive:
            self.hero.current_zone = None
            self.status = "failed"
            print(
                f"    [DEATH] {self.hero.name} was killed by "
                f"{zone.event_creature_name}."
            )
            return

        if zone.event_creature_health <= 0.0:
            zone.event_creature_active = False
            self.world.event_creature_zone_id = None
            self.creature_defeated = True
            print(
                f"    [VICTORY] {self.hero.name} has defeated "
                f"{zone.event_creature_name}!"
            )

    def _resolve(self) -> None:
        """Finalise the expedition and award rewards."""

        self.loot = {}

        if self.target_zone.event_creature_active:
            print(
                f"    [BLOCKED] {self.target_zone.event_creature_name} "
                f"still holds {self.target_zone.name}; no resources can be looted."
            )
            return

        for resource, node_value in (
            self.target_zone.resource_nodes.items()
        ):

            if node_value <= 0:

                continue

            max_turns = MAX_EXPEDITION_TURNS_PER_TIER.get(
                self.target_zone.tier, 10
            )
            t = self.duration_turns / max_turns
            log_mult = math.log(1 + t * 9) / math.log(10)

            harvest = min(
                node_value,
                int(node_value * 0.3 * log_mult) + 1
            )

            if (
                resource == Resource.KNOWLEDGE
                and self.hero.specialization == "Researcher"
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

        if self.creature_defeated:
            multiplier = random.uniform(5.0, 7.0)
            for resource in self.loot:
                self.loot[resource] = int(self.loot[resource] * multiplier)
            print(
                f"    [BOUNTY] Creature defeated! Loot multiplied "
                f"by {multiplier:.2f}x!"
            )

        xp_gain = int(
            self.target_zone.danger_rating
            * self.target_zone.tier
            * 5
        )

        self.hero.gain_experience(xp_gain)
        self.hero.expeditions_completed += 1

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

    def __init__(self, level_id: int, name: str,
                 aether_density: float, guardian_power_level: float,
                 resource_nodes: dict | None = None,
                 structural_mods: list | None = None,
                 active_events: list | None = None) -> None:
        self.level_id = level_id
        self.name = name
        self.aether_density = aether_density
        self.guardian_power_level = guardian_power_level
        self.resource_nodes = resource_nodes if resource_nodes is not None else {}  #consider changing resource nodes to 'surrounding resource nodes', referring to materials that can be gained in surrounding levels
        self.structural_mods = structural_mods if structural_mods is not None else []
        self.active_events = active_events if active_events is not None else []

    def to_dict(self) -> dict:
        """Serialize level to a JSON-safe dict."""
        return {
            "level_id": self.level_id,
            "name": self.name,
            "aether_density": self.aether_density,
            "guardian_power_level": self.guardian_power_level,
            "resource_nodes": {
                r.value: qty
                for r, qty in self.resource_nodes.items()
            },
            "structural_mods": self.structural_mods,
            "active_events": self.active_events,    #referring to events that are affecting this level directly.
        }

    @classmethod
    def from_dict(cls, data: dict) -> DungeonLevel:
        """Deserialize a level from a dict."""
        return cls(
            level_id=data["level_id"],
            name=data["name"],
            aether_density=data["aether_density"],
            guardian_power_level=data["guardian_power_level"],
            resource_nodes={
                Resource(k): v
                for k, v
                in data.get("resource_nodes", {}).items()
            },
            structural_mods=data.get("structural_mods", []),
            active_events=data.get("active_events", []),
        )


class WorldZone:
    """A zone within the outside world of the dungeon."""

    def __init__(self, zone_id: int, name: str, tier: int,
                 danger_rating: float,
                 resource_nodes: dict | None = None,
                 is_discovered: bool = False,
                 threat_level: int = 0,
                 event_creature_active: bool = False,
                 event_creature_name: str | None = None,
                 event_creature_health: float = 0.0,
                 event_creature_attack: float = 0.0) -> None:
        self.zone_id = zone_id
        self.name = name
        self.tier = tier
        self.danger_rating = danger_rating
        self.resource_nodes = resource_nodes if resource_nodes is not None else {}
        self.is_discovered = is_discovered
        self.threat_level = threat_level       #add an events side to this. It could describe possible events that could come from this zone.
        self.event_creature_active = event_creature_active
        self.event_creature_name = event_creature_name
        self.event_creature_health = event_creature_health
        self.event_creature_attack = event_creature_attack

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
            "event_creature_active": self.event_creature_active,
            "event_creature_name": self.event_creature_name,
            "event_creature_health": self.event_creature_health,
            "event_creature_attack": self.event_creature_attack,
        }

    @classmethod
    def from_dict(cls, data: dict) -> WorldZone:
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
            event_creature_active=data.get("event_creature_active", False),
            event_creature_name=data.get("event_creature_name"),
            event_creature_health=data.get("event_creature_health", 0.0),
            event_creature_attack=data.get("event_creature_attack", 0.0),
        )


class DungeonWorld:
    """A named dungeon world containing multiple levels and zones."""

    def __init__(self, name: str = "", levels: dict | None = None,
                 turn: int = 0, zones: dict | None = None,
                 known_zones: list | None = None,
                 active_expeditions: list | None = None,
                 stockpile: dict | None = None,
                 event_zone_ids: list | None = None,
                 event_progress: float = 0.0,
                 event_triggered: bool = False,
                 event_creature_zone_id: int | None = None,
                 expedition_supplies: int = 50) -> None:
        self.name = name   #of the dungeon world taken from the load.
        self.levels = levels if levels is not None else {}
        self.turn = turn
        self.zones = zones if zones is not None else {}
        self.known_zones = known_zones if known_zones is not None else []
        self.active_expeditions = (
            active_expeditions
            if active_expeditions is not None
            else []
        )
        self.stockpile = (   #for the dungeon. Not the whole world. But I think I need to make that clearer.
            stockpile
            if stockpile is not None
            else {r: 0 for r in Resource}
        )
        self.heroes = []
        self.guardians = []
        self.builders = []    #other units will follow
        self.next_unit_id = 1
        self.event_zone_ids = event_zone_ids if event_zone_ids is not None else []
        self.event_progress = event_progress
        self.event_triggered = event_triggered
        self.event_creature_zone_id = event_creature_zone_id
        self.expedition_supplies = expedition_supplies

    def get_next_unit_id(self) -> int:
        uid = self.next_unit_id
        self.next_unit_id += 1
        return uid

    def create_hero(self, name: str, specialization: str) -> Hero:
        hero = Hero(self.get_next_unit_id(), name, specialization)
        self.heroes.append(hero)
        return hero

    def create_builder(self, build_speed: float = 1.0) -> Builder:
        builder = Builder(self.get_next_unit_id(), build_speed=build_speed)
        self.builders.append(builder)
        return builder

    def find_hero(self, hero_id: int):
        for hero in self.heroes:
            if hero.unit_id == hero_id:
                return hero
        return None

    def find_zone(self, zone_id: int):
        return self.zones.get(zone_id)

    def send_hero_on_expedition(
        self,
        hero_id: int,
        zone_id: int,
        duration: int,
    ):
        if duration <= 0:
            raise ValueError("Duration must be a positive integer.")

        hero = self.find_hero(hero_id)
        if hero is None:
            raise ValueError(f"No hero with ID {hero_id}.")

        if not hero.is_alive:
            raise ValueError(f"{hero.name} is dead and cannot be sent.")

        if hero.current_zone is not None:
            raise ValueError(
                f"{hero.name} is already on an expedition."
            )

        target_zone = self.find_zone(zone_id)
        if target_zone is None:
            raise ValueError(f"No zone with ID {zone_id}.")

        # Duration cap check
        max_turns = MAX_EXPEDITION_TURNS_PER_TIER.get(target_zone.tier, 10)
        if duration > max_turns:
            raise ValueError(
                f"Max duration for tier {target_zone.tier} zones "
                f"is {max_turns} turns."
            )

        # Expedition supply pool check
        supply_cost = duration * SUPPLY_COST_PER_TURN
        if self.expedition_supplies < supply_cost:
            raise ValueError(
                f"Not enough supplies. Need {supply_cost}, "
                f"have {self.expedition_supplies}."
            )

        # Stockpile resource cost check
        shortfalls: list[str] = []
        for r in EXPEDITION_COST_RESOURCES:
            cost = duration * target_zone.tier
            if self.stockpile.get(r, 0) < cost:
                shortfalls.append(
                    f"{r.value} ({self.stockpile.get(r, 0)}/{cost})"
                )
        if shortfalls:
            raise ValueError(
                f"Missing resources: {', '.join(shortfalls)}"
            )

        # Deduct costs
        self.expedition_supplies -= supply_cost
        print(f"    [COST] Supplies: -{supply_cost} (remaining: {self.expedition_supplies})")
        for r in EXPEDITION_COST_RESOURCES:
            cost = duration * target_zone.tier
            self.stockpile[r] -= cost
            print(f"    [COST] {r.value}: -{cost}")

        hero.current_zone = zone_id
        if not self.event_triggered and zone_id in self.event_zone_ids:
            self._increase_event_progress(zone_id)

        expedition = Expedition(
            hero=hero,
            target_zone=target_zone,
            world=self,
            duration_turns=duration,
        )
        self.active_expeditions.append(expedition)
        return expedition

    def _increase_event_progress(self, zone_id: int) -> None:
        """Increase the rare event progress for initial tier 1 zones."""
        self.event_progress = min(1.0, self.event_progress + 0.2)
        print(
            f"  [EVENT] Expedition into initial zone {zone_id} "
            f"raises the stirring chance to {self.event_progress:.1f}."
        )

        if self.event_progress >= 1.0:
            self._trigger_event(zone_id)

    def _trigger_event(self, zone_id: int) -> None:
        """Activate the one-time creature event in a primary zone."""
        self.event_triggered = True
        self.event_creature_zone_id = zone_id

        zone = self.zones.get(zone_id)
        if zone is None:
            return

        zone.event_creature_active = True
        zone.event_creature_name = "Roused Aberration"
        zone.event_creature_health = 20.0 + zone.tier * 12.0 + zone.danger_rating
        zone.event_creature_attack = 6.0 + zone.tier * 3.0 + zone.danger_rating * 0.25
        zone.threat_level = max(zone.threat_level, 2)

        print(
            f"\n--- EVENT TRIGGERED ---"
            f"\nA {zone.event_creature_name} has awakened in {zone.name}."
            f"\nHeroes will face it on the next expedition there."
        )

    def has_active_expeditions(self) -> bool:
        return bool(self.active_expeditions)

    def get_active_expeditions(self):
        return list(self.active_expeditions)

    def advance_turn(self) -> None:
        self.tick()

    def to_dict(self) -> dict:
        """Serialize world to a JSON-safe dict."""
        return {
            "name": self.name,
            "turn": self.turn,
            "next_unit_id": self.next_unit_id,
            "levels": {
                str(lvl_id): level.to_dict()
                for lvl_id, level in self.levels.items()
            },
            "zones": {
                str(zone_id): zone.to_dict()
                for zone_id, zone in self.zones.items()
            },
            "known_zones": self.known_zones,
            "heroes": [hero.to_dict() for hero in self.heroes],
            "guardians": [guard.to_dict() for guard in self.guardians],
            "builders": [builder.to_dict() for builder in self.builders],
            "active_expeditions": [     #might soon need to implement feature to handle multiple heroes on a single expedition.
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
                    "has_engaged_event_creature": exp.has_engaged_event_creature,
                    "creature_defeated": exp.creature_defeated,
                    "loot": {
                        (r.value if isinstance(r, Resource) else r): qty
                        for r, qty in exp.loot.items()
                    },
                }
                for exp in self.active_expeditions
            ],
            "event_zone_ids": self.event_zone_ids,
            "event_progress": self.event_progress,
            "event_triggered": self.event_triggered,
            "event_creature_zone_id": self.event_creature_zone_id,
            "expedition_supplies": self.expedition_supplies,
            "stockpile": {
                r.value: qty
                for r, qty in self.stockpile.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> DungeonWorld:
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

        world = cls(name=name, levels=levels, turn=turn,
                    zones=zones, known_zones=known_zones,
                    stockpile=stockpile,
                    event_zone_ids=data.get("event_zone_ids", []),
                    event_progress=data.get("event_progress", 0.0),
                    event_triggered=data.get("event_triggered", False),
                    event_creature_zone_id=data.get("event_creature_zone_id"),
                    expedition_supplies=data.get("expedition_supplies", 0),
                    )

        # Reconstruct dynamic unit state and unique ID counter
        world.next_unit_id = data.get("next_unit_id", 1)

        world.heroes = []
        for hero_data in data.get("heroes", []):
            world.heroes.append(Hero.from_dict(hero_data))

        world.guardians = []
        for guard_data in data.get("guardians", []):
            world.guardians.append(Guardian.from_dict(guard_data))

        world.builders = []
        for builder_data in data.get("builders", []):
            world.builders.append(Builder.from_dict(builder_data))  #will add more units over here as well

        # Reconstruct active expeditions with object links resolved
        world.active_expeditions = []
        for exp_data in data.get("active_expeditions", []):
            hero_id = exp_data.get("hero_id")
            target_zone_id = exp_data.get("target_zone_id")

            # Find the actual Hero and WorldZone instances in world_data
            found_hero = None
            for h in world.heroes:
                if h.unit_id == hero_id:
                    found_hero = h
                    break
            found_zone = world.zones.get(target_zone_id)

            if found_hero and found_zone:
                exp = Expedition(
                    hero=found_hero,
                    target_zone=found_zone,
                    world=world,
                    duration_turns=exp_data.get("duration_turns", 0),
                    turns_elapsed=exp_data.get("turns_elapsed", 0),
                    status=exp_data.get("status", "active"),
                    loot={
                        Resource(k): v
                        for k, v in exp_data.get("loot", {}).items()
                    },
                    has_engaged_event_creature=exp_data.get(
                        "has_engaged_event_creature", False
                    ),
                    creature_defeated=exp_data.get(
                        "creature_defeated", False
                    ),
                )
                world.active_expeditions.append(exp)

        return world

    def tick(self) -> None:
        """Advance the game by one turn."""

        self.turn += 1

        self._process_environmental_events()

        self._process_expeditions(self.heroes)

        self._process_unit_statuses(
            self.heroes, self.guardians, self.builders
        )

        print(f"\n--- Turn {self.turn} ---")

    def _process_expeditions(self, heroes):
        """Advance all active expeditions, removing completed or failed ones."""

        completed = []

        for exp in self.active_expeditions:

            exp.advance()

            if exp.status in ("returned", "failed"):   #will need to define exactly what 'failure' and 'success' are.

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

    def _process_environmental_events(self) -> None:
        """Dispatch environmental events each tick."""

        for exp in self.active_expeditions:
            if (
                exp.target_zone.event_creature_active
                and not exp.has_engaged_event_creature
            ):
                exp._resolve_event_creature_encounter()

    def _process_unit_statuses(
        self, heroes, guardians, builders
    ):
        """Apply per-tick effects to all units."""

        for unit in heroes:
            unit.apply_tick_effects()

        for unit in guardians:
            unit.apply_tick_effects()

        for unit in builders:
            unit.apply_tick_effects()
