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
├── entities.py        # Core domain model, game state, and serialization
├── generation.py      # Procedural generation of dungeon levels and outside zones
├── save_load.py       # JSON persistence with transactional save semantics
├── migrations.py      # Save schema migration pipeline (v1 → v2)
├── display.py         # Terminal display helpers
├── recruitment.py     # Interactive hero/builder recruitment flows
├── constants.py       # Resource enum, specialization list, word lists
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
| Tick-phase hooks are placeholders | `entities.py` | Environmental events and unit status processing are not implemented |
| No LICENSE file | repository root | Legal status is undefined |
| No CI workflow | repository root | Automated checks are not enabled |
| Documentation needs syncing | `README.md`, `AGENTS.md` | Current commands and behavior may be outdated |

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
| `save` | Save the current world |
| `exit` | Save and quit the game |

## Serialization

- Most core classes implement `to_dict()` / `from_dict()` for JSON persistence.
- `Resource` values serialize as strings and restore via `Resource(k)`.
- `DungeonWorld.from_dict()` reconstructs heroes, guardians, builders, and active expeditions.
- Save files include `schema_version` and can be migrated from older save formats.
- Saves are written transactionally with a `.tmp` file and `os.replace()`.

## Key Facts

- **Standard library only** at runtime.
- **`pyproject.toml` exists** and declares dev extras for `pytest` and `mypy`.
- `DungeonWorld` owns levels, zones, heroes, guardians, builders, expeditions, and stockpile state.
- `send` dispatches heroes to discovered zones and resolves loot on tick.
- `create_builder()` no longer prompts for a name; builders are identified by ID only.
- `Researcher` specialization already doubles `KNOWLEDGE` harvest in current expedition logic.
- `MAX_LEVEL = 3` controls generated dungeon size; existing saves can preserve their own layout.
