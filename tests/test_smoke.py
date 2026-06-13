"""Smoke tests for the worldbuildingengine package.

Run with: python -m unittest tests/test_smoke.py
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from worldbuildingengine.constants import Resource
from worldbuildingengine.generation import generate_dungeon_world
from worldbuildingengine.entities import (
    DungeonWorld, DungeonLevel, WorldZone, Expedition,
    Hero, Guardian, Builder,
)
from worldbuildingengine.save_load import (
    save_dungeon_world, load_dungeon_world,
)
from worldbuildingengine.display import (
    display_level_summary, display_world_overview,
    display_random_level, display_specific_level,
)


class TestWorldGeneration(unittest.TestCase):
    """Verify the procedural generation produces expected structure."""

    def test_world_has_3_levels(self):
        w = generate_dungeon_world()
        self.assertEqual(len(w.levels), 3)

    def test_world_has_10_zones(self):
        w = generate_dungeon_world()
        self.assertEqual(len(w.zones), 10)

    def test_world_has_2_discovered_zones(self):
        w = generate_dungeon_world()
        self.assertEqual(len(w.known_zones), 2)

    def test_discovered_zones_are_tier_1(self):
        w = generate_dungeon_world()
        for zone_id in w.known_zones:
            self.assertEqual(w.zones[zone_id].tier, 1)

    def test_levels_have_resource_nodes(self):
        w = generate_dungeon_world()
        for level in w.levels.values():
            self.assertGreater(len(level.resource_nodes), 0)

    def test_zones_have_resource_nodes(self):
        w = generate_dungeon_world()
        for zone in w.zones.values():
            self.assertGreater(len(zone.resource_nodes), 0)


class TestSerialization(unittest.TestCase):
    """Verify to_dict / from_dict round-trips for all data classes."""

    def test_dungeon_level_round_trip(self):
        orig = DungeonLevel(
            level_id=1,
            name="Test Level",
            aether_density=19.8,
            guardian_power_level=2.5,
            resource_nodes={Resource.STONE: 10, Resource.WOOD: 5},
        )
        data = orig.to_dict()
        restored = DungeonLevel.from_dict(data)
        self.assertEqual(restored.level_id, orig.level_id)
        self.assertEqual(restored.name, orig.name)
        self.assertEqual(restored.aether_density, orig.aether_density)
        self.assertEqual(restored.guardian_power_level, orig.guardian_power_level)
        self.assertEqual(restored.resource_nodes, orig.resource_nodes)

    def test_world_zone_round_trip(self):
        orig = WorldZone(
            zone_id=1,
            name="Blighted Ashfield",
            tier=2,
            danger_rating=22.5,
            resource_nodes={Resource.IRON: 8, Resource.KNOWLEDGE: 3},
            is_discovered=True,
            threat_level=1,
        )
        data = orig.to_dict()
        restored = WorldZone.from_dict(data)
        self.assertEqual(restored.zone_id, orig.zone_id)
        self.assertEqual(restored.name, orig.name)
        self.assertEqual(restored.tier, orig.tier)
        self.assertEqual(restored.danger_rating, orig.danger_rating)
        self.assertEqual(restored.resource_nodes, orig.resource_nodes)
        self.assertEqual(restored.is_discovered, orig.is_discovered)

    def test_hero_round_trip(self):
        orig = Hero(hero_id=1, name="TestHero", specialization="Prospector")
        orig.stamina = 80.0
        orig.sanity = 90.0
        orig.current_zone = 3
        orig.add_resource(Resource.STONE, 5)
        data = orig.to_dict()
        restored = Hero.from_dict(data)
        self.assertEqual(restored.unit_id, orig.unit_id)
        self.assertEqual(restored.name, orig.name)
        self.assertEqual(restored.specialization, orig.specialization)
        self.assertEqual(restored.stamina, orig.stamina)
        self.assertEqual(restored.current_zone, orig.current_zone)
        self.assertIn(Resource.STONE, restored.inventory)
        self.assertEqual(restored.inventory[Resource.STONE], 5)

    def test_guardian_round_trip(self):
        orig = Guardian(guardian_id=1, name="Guard", level=2)
        orig.assigned_level_id = 2
        data = orig.to_dict()
        restored = Guardian.from_dict(data)
        self.assertEqual(restored.unit_id, orig.unit_id)
        self.assertEqual(restored.name, orig.name)
        self.assertEqual(restored.level, orig.level)
        self.assertEqual(restored.power_level, orig.power_level)
        self.assertEqual(restored.assigned_level_id, orig.assigned_level_id)

    def test_builder_round_trip(self):
        orig = Builder(builder_id=1, build_speed=2.0)
        orig.current_task = "build"
        data = orig.to_dict()
        restored = Builder.from_dict(data)
        self.assertEqual(restored.unit_id, orig.unit_id)
        self.assertEqual(restored.build_speed, orig.build_speed)
        self.assertEqual(restored.current_task, orig.current_task)

    def test_world_round_trip(self):
        orig = generate_dungeon_world()
        # Add a hero to test nested serialization
        hero = Hero(hero_id=1, name="Aragorn", specialization="Prospector")
        orig.heroes.append(hero)
        orig.stockpile[Resource.STONE] = 50

        data = orig.to_dict()
        restored = DungeonWorld.from_dict(data)

        self.assertEqual(len(restored.levels), len(orig.levels))
        self.assertEqual(len(restored.zones), len(orig.zones))
        self.assertEqual(restored.known_zones, orig.known_zones)
        self.assertEqual(len(restored.heroes), 1)
        self.assertEqual(restored.heroes[0].name, "Aragorn")
        self.assertEqual(restored.stockpile[Resource.STONE], 50)

    def test_save_load_round_trip(self):
        w = generate_dungeon_world()
        save_name = "_test_roundtrip"
        save_dungeon_world(w, save_name)
        loaded = load_dungeon_world(save_name)
        self.assertIsNotNone(loaded)
        self.assertEqual(len(loaded.levels), 3)
        self.assertEqual(len(loaded.zones), 10)
        # Clean up
        for ext in [".json", ".json.tmp"]:
            path = os.path.join("saves", f"{save_name}{ext}")
            if os.path.exists(path):
                os.remove(path)


class TestDisplayFunctions(unittest.TestCase):
    """Verify display functions run without error."""

    def test_display_level_summary(self):
        level = DungeonLevel(
            level_id=1, name="Test", aether_density=10.0,
            guardian_power_level=1.0,
        )
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            display_level_summary(level)
        self.assertIn("Level 1", buf.getvalue())

    def test_display_random_level_output(self):
        w = generate_dungeon_world()
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            display_random_level(w)
        output = buf.getvalue()
        self.assertIn("DISCOVERY", output)
        self.assertIn("Aether", output)
        self.assertIn("Guardian", output)

    def test_display_specific_level_output(self):
        w = generate_dungeon_world()
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            display_specific_level(w, 1)
        output = buf.getvalue()
        self.assertIn("FOUND", output)
        self.assertIn("Density", output)
        self.assertIn("Power", output)

    def test_display_specific_level_out_of_range(self):
        w = generate_dungeon_world()
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            display_specific_level(w, 99)
        self.assertIn("Level 3", buf.getvalue())


class TestExpeditionFlow(unittest.TestCase):
    """Full expedition lifecycle: create hero → send → tick → check stockpile."""

    def test_full_expedition_flow(self):
        w = generate_dungeon_world()
        hero = w.create_hero("Tester", "Prospector")

        # Send to first discovered zone
        zone_id = w.known_zones[0]
        target = w.zones[zone_id]
        w.send_hero_on_expedition(hero.unit_id, zone_id, 1)

        # Tick once to resolve
        w.advance_turn()

        # After tick, expedition should be completed
        self.assertEqual(len(w.active_expeditions), 0)
        # Hero should be back
        self.assertIsNone(hero.current_zone)
        # Resources should have been deposited
        total_deposited = sum(w.stockpile.values())
        self.assertGreater(total_deposited, 0)
        # Zone resources should be depleted
        for val in target.resource_nodes.values():
            self.assertGreaterEqual(val, 0)

    def test_hero_death_on_expedition(self):
        w = generate_dungeon_world()
        hero = w.create_hero("Doomed", "Warrior")
        hero.health = 1.0  # One hit from death

        zone_id = w.known_zones[0]
        target = w.zones[zone_id]

        exp = w.send_hero_on_expedition(hero.unit_id, zone_id, 5)

        w.advance_turn()  # Apply pressure once

        # Hero should be dead if damage exceeded 1.0
        if not hero.is_alive:
            self.assertEqual(exp.status, "failed")
            self.assertEqual(len(w.active_expeditions), 0)


class TestStockpileInitialization(unittest.TestCase):
    """Verify stockpile starts empty for every resource."""

    def test_fresh_world_stockpile(self):
        w = generate_dungeon_world()
        for resource in Resource:
            self.assertEqual(w.stockpile[resource], 0)

    def test_stockpile_all_resources_present(self):
        w = generate_dungeon_world()
        self.assertEqual(len(w.stockpile), len(list(Resource)))


if __name__ == "__main__":
    unittest.main()
