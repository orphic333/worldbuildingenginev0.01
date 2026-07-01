# AGENTS.md — Worldbuilding Engine

## Entrypoints

```bash
python worldengine.py
python -m worldbuildingengine.main
python -m unittest tests/test_smoke.py
```

## Architecture

```
worldengine.py         ← thin wrapper
worldbuildingengine/
├── main.py            # Startup: world selection, create/load, display initial world state
├── oracle.py          # REPL command dispatch loop
├── entities.py        # Core domain model, game state, serialization, tick logic
├── generation.py      # Procedural generation of dungeon levels, outside zones, and initial stockpile
├── save_load.py       # JSON persistence with transactional save semantics
├── migrations.py      # Save schema migration pipeline (v1 → v2 → v3)
├── display.py         # Terminal display helpers
├── recruitment.py     # Interactive hero/builder recruitment flows
├── constants.py       # Resource enum, categories, initial stockpile, cost tables, word lists
└── types.py           # Minimal type aliases
saves/                  # Saved dungeon worlds in JSON
tests/                  # Smoke tests and future unit tests
pyproject.toml          # Packaging and dev tooling metadata
```

**Current constraint:** `entities.py` still contains the core entity classes to avoid circular imports between `DungeonWorld`, `Hero`, `WorldZone`, and `Expedition`.

## Current Notes

| Issue | File | Effect |
|---|---|---|
| `display_world_zones()` implemented | `display.py` | Shows known zones with details |
| `_process_environmental_events()` dispatches creature encounters | `entities.py` | Active expedition event phase before expedition resolution |
| `_process_unit_statuses()` applies builder decay + guardian maintenance | `entities.py` | Per-tick unit lifecycle and cost deduction |
| No LICENSE file | repository root | Legal status is undefined |
| No CI workflow | repository root | Automated checks are not enabled |

## Build / Test Commands

- **Run the game**: `python worldengine.py`
- **Run the package directly**: `python -m worldbuildingengine.main`
- **Run smoke tests**: `python -m unittest tests/test_smoke.py`
- **Run all tests**: `python -m unittest discover -s tests`

## Oracle Commands

| Command | Action |
|---|---|
| `random` | Show a random dungeon level |
| `recruit` | Recruit a hero or builder |
| `heroes` | List recruited heroes, guardians, and builders |
| `hero <id>` | Show detailed hero status |
| `zones` | List discovered outside zones |
| `send <hero_id> <zone_id> <duration>` | Dispatch a hero on an expedition |
| `expeditions` | Show active expedition status |
| `tick` | Advance one turn and process expeditions |
| `stockpile` | Show accumulated dungeon stockpile resources |
| `harvest <level_id>` | Collect aether crystals from a dungeon level's nodes |
| `nodes <level_id>` | Show detailed aether crystal node status for a level |
| `save` | Save the current world |
| `exit` | Save and quit the game |

## Serialization

- Most core classes implement `to_dict()` / `from_dict()` for JSON persistence.
- `Resource` values serialize as strings and restore via `Resource(k)`.
- `DungeonWorld.from_dict()` reconstructs heroes, guardians, builders, and active expeditions.
- Save files include `schema_version` and can be migrated from older save formats (`v1` → `v2` → `v3`).
- Saves are written transactionally with a `.tmp` file and `os.replace()`.
- `Guardian.to_dict()` now includes `maintenance_resource` (Resource enum value, serialized as string).

## Key Facts

- **Standard library only** at runtime.
- **`pyproject.toml` exists** and declares dev extras for `pytest` and `mypy`.
- `DungeonWorld` owns levels, zones, heroes, guardians, builders, expeditions, and stockpile state.
- `send` dispatches heroes to discovered zones and resolves loot on tick.
- `create_builder()` no longer prompts for a name; builders are identified by ID only.
- `Researcher` specialization already doubles `KNOWLEDGE` harvest in current expedition logic.
- `MAX_LEVEL = 3` controls generated dungeon size; existing saves can preserve their own layout.
- **Expedition costs:** separate `expedition_supplies` pool + stockpile resources (wood, fibre, meat, water). Costs = `duration × tier` (stockpile) + `duration × SUPPLY_COST_PER_TURN` (supplies). Duration capped per tier: 5/10/15.
- **Escalating zone pressure:** Per-turn damage multiplied by `1 + log(1 + turns_elapsed)` with 80–120% jitter. Logarithmic harvest scaling: `log_mult = log(1 + t×9) / log(10)` where `t = duration / max_turns`.
- **Guardian maintenance:** Per-tick, alive-and-assigned guardians cost 1 blood (flat) + `int(aether_density ** 1/3)` of their `maintenance_resource` (defaults to STONE). Both deducted from stockpile.
- **Initial stockpile:** New worlds seed via `INITIAL_STOCKPILE` dict in `constants.py`. Tiers: Common 80 (stone, water, wood, soft_rock, hard_rock), Uncommon 40 (iron, copper, meat, blood, aether_crystals), Rare 15 (rare_metals), Trace 5 (aetherite).
- **Resource categories:** `ResourceCategory` enum (`CONSUMABLE`/`STATIC`). `KNOWLEDGE` is the only STATIC resource. `CONSUMABLE_RESOURCES` list drives stockpile display filtering.
- **`_process_unit_statuses()`** handles builder decay (lifespan −1 every 2 ticks), guardian `apply_tick_effects()`, and guardian maintenance cost deduction.
- **`_process_environmental_events()`** dispatches creature encounters for active expeditions targeting event-occupied zones before expedition resolution.
- **Aether crystal nodes:** `DungeonLevel.aether_crystal_nodes` is a list of `{"current", "max_capacity", "growth_rate"}` dicts. Number of nodes, max per node, and growth rate all scale with level number. Nodes grow each tick in `_process_dungeon_resources()` (called after unit statuses). `harvest <level_id>` empties nodes into stockpile.
