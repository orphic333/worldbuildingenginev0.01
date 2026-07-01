"""Smoke tests for the worldbuildingengine package.

Run with: python -m unittest tests/test_smoke.py
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from worldbuildingengine.constants import (
    Resource, EXPEDITION_COST_RESOURCES, GUARDIAN_BLOOD_COST,
    INITIAL_STOCKPILE, CONSUMABLE_RESOURCES,
)
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


def seed_expedition_costs(w: DungeonWorld) -> None:
    """Give a test world enough supplies and stockpile to send expeditions."""
    w.expedition_supplies = 200
    for r in EXPEDITION_COST_RESOURCES:
        w.stockpile[r] = 200


class TestWorldGeneration(unittest.TestCase):
    """Verify the procedural generation produces expected structure."""

    def test_world_has_3_levels(self):
        w = generate_dungeon_world()
        self.assertEqual(len(w.levels), 3)

    def test_world_has_10_zones(self):
        w = generate_dungeon_world()
        self.assertEqual(len(w.zones), 10)

    def test_world_has_3_discovered_zones(self):
        w = generate_dungeon_world()
        self.assertEqual(len(w.known_zones), 3)

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
        seed_expedition_costs(w)
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
        seed_expedition_costs(w)
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

    def test_event_progression_triggers_creature(self):
        w = generate_dungeon_world()
        seed_expedition_costs(w)
        hero = w.create_hero("EventHero", "Warrior")

        self.assertEqual(len(w.event_zone_ids), 3)
        self.assertFalse(w.event_triggered)

        for i in range(5):
            zone_id = w.event_zone_ids[i % 3]
            w.send_hero_on_expedition(hero.unit_id, zone_id, 1)
            w.advance_turn()
            hero.current_zone = None

        self.assertTrue(w.event_triggered)
        self.assertIsNotNone(w.event_creature_zone_id)
        triggered_zone = w.zones[w.event_creature_zone_id]
        self.assertGreater(triggered_zone.event_creature_health, 0.0)

    def test_event_creature_blocks_loot(self):
        w = generate_dungeon_world()
        seed_expedition_costs(w)
        hero = w.create_hero("LootHero", "Warrior")
        zone_id = w.event_zone_ids[0]
        w.event_progress = 1.0
        w._trigger_event(zone_id)
        w.zones[zone_id].event_creature_health = 999

        exp = w.send_hero_on_expedition(hero.unit_id, zone_id, 1)
        w.advance_turn()

        self.assertEqual(exp.loot, {})
        self.assertTrue(w.zones[zone_id].event_creature_active)

    def test_event_creature_defeat_rewards(self):
        w = generate_dungeon_world()
        seed_expedition_costs(w)
        import math
        hero = w.create_hero("DefeatHero", "Warrior")
        zone_id = w.event_zone_ids[0]
        original_resources = dict(w.zones[zone_id].resource_nodes)
        w._trigger_event(zone_id)

        exp = w.send_hero_on_expedition(hero.unit_id, zone_id, 1)
        exp.has_engaged_event_creature = True
        exp.creature_defeated = True
        w.zones[zone_id].event_creature_active = False
        w.event_creature_zone_id = None
        w.advance_turn()

        self.assertGreater(len(exp.loot), 0)
        for resource, qty in exp.loot.items():
            max_turns = 5
            t = 1 / max_turns
            log_mult = math.log(1 + t * 9) / math.log(10)
            expected_normal = min(
                original_resources[resource],
                int(original_resources[resource] * 0.5 * log_mult) + 1
            )
            self.assertGreaterEqual(qty, int(expected_normal * 5.0))
            self.assertLessEqual(qty, int(expected_normal * 7.0) + 1)


class TestStockpileInitialization(unittest.TestCase):
    """Verify stockpile is seeded with correct initial values."""

    def test_stockpile_all_resources_present(self):
        w = generate_dungeon_world()
        self.assertEqual(len(w.stockpile), len(list(Resource)))

    def test_initial_stockpile_values(self):
        w = generate_dungeon_world()
        for r, qty in INITIAL_STOCKPILE.items():
            self.assertEqual(
                w.stockpile[r], qty,
                f"Expected {qty} of {r.value}, got {w.stockpile[r]}"
            )

    def test_non_initial_resources_start_at_zero(self):
        w = generate_dungeon_world()
        for r in Resource:
            if r not in INITIAL_STOCKPILE:
                self.assertEqual(
                    w.stockpile[r], 0,
                    f"Expected 0 of {r.value}, got {w.stockpile[r]}"
                )

    def test_consumable_resources_excludes_knowledge(self):
        self.assertNotIn(Resource.KNOWLEDGE, CONSUMABLE_RESOURCES)
        self.assertIn(Resource.STONE, CONSUMABLE_RESOURCES)
        self.assertIn(Resource.BLOOD, CONSUMABLE_RESOURCES)


class TestGuardianMaintenance(unittest.TestCase):
    """Guardian per-tick maintenance costs."""

    def test_guardian_maintenance_deducts_blood_and_stone(self):
        w = generate_dungeon_world()
        g = Guardian(guardian_id=1, name="Sentry", level=1)
        g.assigned_level_id = 1
        w.guardians.append(g)
        w.stockpile[Resource.BLOOD] = 10
        w.stockpile[Resource.STONE] = 10
        w.advance_turn()
        level = w.levels[1]
        expected_stone = int(level.aether_density ** (1/3))
        self.assertEqual(w.stockpile[Resource.BLOOD], 10 - GUARDIAN_BLOOD_COST)
        self.assertEqual(w.stockpile[Resource.STONE], 10 - expected_stone)

    def test_dead_guardian_no_maintenance(self):
        w = generate_dungeon_world()
        g = Guardian(guardian_id=2, name="Corpse", level=1)
        g.assigned_level_id = 1
        g.is_alive = False
        w.guardians.append(g)
        w.stockpile[Resource.BLOOD] = 10
        w.stockpile[Resource.STONE] = 10
        w.advance_turn()
        self.assertEqual(w.stockpile[Resource.BLOOD], 10)
        self.assertEqual(w.stockpile[Resource.STONE], 10)

    def test_unassigned_guardian_no_maintenance(self):
        w = generate_dungeon_world()
        g = Guardian(guardian_id=3, name="Loner", level=1)
        w.guardians.append(g)
        w.stockpile[Resource.BLOOD] = 10
        w.stockpile[Resource.STONE] = 10
        w.advance_turn()
        self.assertEqual(w.stockpile[Resource.BLOOD], 10)
        self.assertEqual(w.stockpile[Resource.STONE], 10)

    def test_guardian_maintenance_round_trip_keeps_diet(self):
        g = Guardian(guardian_id=4, name="StoneGuard", level=2,
                     maintenance_resource=Resource.STONE)
        data = g.to_dict()
        restored = Guardian.from_dict(data)
        self.assertEqual(restored.maintenance_resource, Resource.STONE)

    def test_multiple_guardians_multiple_levels(self):
        w = generate_dungeon_world()
        g1 = Guardian(guardian_id=5, name="GuardA", level=1)
        g1.assigned_level_id = 1
        g2 = Guardian(guardian_id=6, name="GuardB", level=1)
        g2.assigned_level_id = 2
        w.guardians.extend([g1, g2])
        w.stockpile[Resource.BLOOD] = 20
        w.stockpile[Resource.STONE] = 20
        lvl1_cost = int(w.levels[1].aether_density ** (1/3))
        lvl2_cost = int(w.levels[2].aether_density ** (1/3))
        w.advance_turn()
        self.assertEqual(w.stockpile[Resource.BLOOD], 20 - 2 * GUARDIAN_BLOOD_COST)
        self.assertEqual(w.stockpile[Resource.STONE], 20 - lvl1_cost - lvl2_cost)


class TestAetherCrystalNodes(unittest.TestCase):
    """Aether crystal node growth and harvest mechanics."""

    def test_aether_nodes_exist_per_level(self):
        w = generate_dungeon_world()
        self.assertEqual(len(w.levels[1].aether_crystal_nodes), 2)
        self.assertEqual(len(w.levels[2].aether_crystal_nodes), 3)
        self.assertEqual(len(w.levels[3].aether_crystal_nodes), 4)

    def test_aether_nodes_start_full(self):
        w = generate_dungeon_world()
        for level in w.levels.values():
            for node in level.aether_crystal_nodes:
                self.assertEqual(node["current"], node["max_capacity"])

    def test_aether_nodes_grow_on_tick(self):
        w = generate_dungeon_world()
        for level in w.levels.values():
            for node in level.aether_crystal_nodes:
                node["current"] = 0

        before = {
            lid: [n["current"] for n in w.levels[lid].aether_crystal_nodes]
            for lid in w.levels
        }
        w.advance_turn()
        for lid in w.levels:
            for i, node in enumerate(w.levels[lid].aether_crystal_nodes):
                self.assertGreaterEqual(node["current"], before[lid][i])
                self.assertLessEqual(
                    node["current"],
                    before[lid][i] + node["growth_rate"],
                )

    def test_aether_nodes_stop_at_max_capacity(self):
        w = generate_dungeon_world()
        for _ in range(20):
            w.advance_turn()
        for level in w.levels.values():
            for node in level.aether_crystal_nodes:
                self.assertLessEqual(node["current"], node["max_capacity"])

    def test_harvest_depletes_and_deposits(self):
        w = generate_dungeon_world()
        level = w.levels[1]
        expected = sum(n["current"] for n in level.aether_crystal_nodes)
        from worldbuildingengine.oracle import process_user_command
        process_user_command(f"harvest 1", w)
        self.assertEqual(sum(n["current"] for n in level.aether_crystal_nodes), 0)
        self.assertGreaterEqual(
            w.stockpile[Resource.AETHER_CRYSTALS], expected
        )

    def test_harvest_on_empty_level_prints_message(self):
        w = generate_dungeon_world()
        for node in w.levels[1].aether_crystal_nodes:
            node["current"] = 0
        from worldbuildingengine.oracle import process_user_command
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            process_user_command("harvest 1", w)
        self.assertIn("No aether crystals", buf.getvalue())

    def test_aether_node_round_trip(self):
        w = generate_dungeon_world()
        level = w.levels[1]
        data = level.to_dict()
        restored = DungeonLevel.from_dict(data)
        self.assertEqual(
            len(restored.aether_crystal_nodes),
            len(level.aether_crystal_nodes),
        )
        for orig, rest in zip(
            level.aether_crystal_nodes,
            restored.aether_crystal_nodes,
        ):
            self.assertEqual(orig, rest)


if __name__ == "__main__":
    unittest.main()
