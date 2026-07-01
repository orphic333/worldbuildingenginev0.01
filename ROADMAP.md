# ROADMAP.md — Worldbuilding Engine v0.01

> Analysis date: 2026-06-27
> Based on current repository state and implemented code changes.

---

## 1. Codebase Overview

### Purpose

A terminal-based dungeon management simulation. The player runs a dungeon, recruits units, dispatches heroes on outside-world expeditions, extracts resources, and manages turn-based progression through the Oracle REPL.

### Intended Users

Solo player / game dev prototyping. Not yet a production release.

### Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Persistence | JSON files in `saves/` directory |
| Concurrency | None (single-threaded) |
| Testing | Smoke tests and targeted event tests in `tests/test_smoke.py` |
| Packaging | Flat package (`worldbuildingengine/`) with `pyproject.toml` |

No runtime external dependencies. Dev extras are declared in `pyproject.toml`.

### Architecture

```
worldengine.py  (thin wrapper)
  └── worldbuildingengine/
        ├── main.py         — Startup selection and new world creation
        ├── oracle.py       — REPL command loop and user input handling
        ├── entities.py     — Core game domain, state, turn/tick logic, events
        ├── generation.py   — Procedural generation of dungeon levels and world zones
        ├── save_load.py    — Transactional JSON persistence and load logic
        ├── migrations.py   — Save schema migration pipeline (v1 → v2)
        ├── display.py      — Terminal display helpers for world overview and zones
        ├── recruitment.py  — Hero/builder recruitment flows
        ├── constants.py    — Resource enum, specializations, text constants
        └── tests/          — project smoke and integration-style tests
```

**Design pattern:** Thin CLI layer delegates to a monolithic domain model in `entities.py`. Serialization uses `to_dict()` / `from_dict()` for most entities.

**Key architectural notes:**
- `DungeonWorld` now tracks event state for a one-shot expedition creature encounter.
- `WorldZone` contains event-creature fields and can block loot when an event creature is active.
- `generation.py` creates 3 dungeon levels and 10 zones, with 3 initial Tier 1 zones seeded for the event.
- Save logic stamps `schema_version` and writes saves atomically.

### Entity Relationships (Simplified)

```
DungeonWorld
 ├── levels: dict[int, DungeonLevel]
 ├── zones: dict[int, WorldZone]
 ├── heroes: list[Hero]
 ├── guardians: list[Guardian]
 ├── builders: list[Builder]
 ├── active_expeditions: list[Expedition]
 ├── stockpile: dict[Resource, int]
 ├── event_zone_ids: list[int]
 ├── event_progress: float
 ├── event_triggered: bool
 └── turn: int
```

### Entry Points

| Command | Effect |
|---|---|
| `python worldengine.py` | Launch the thin wrapper |
| `python -m worldbuildingengine.main` | Run the game package directly |

### Notable Config

- `SAVE_FOLDER = "saves"`
- `MAX_LEVEL = 3`
- `CURRENT_SCHEMA_VERSION = 3`
- `INITIAL_SUPPLIES = 50`, `SUPPLY_COST_PER_TURN = 3`
- `MAX_EXPEDITION_TURNS_PER_TIER = {1: 5, 2: 10, 3: 15}`
- Expedition costs consume `WOOD`, `FIBRE`, `MEAT`, `WATER` from stockpile + expedition_supplies pool
- `GUARDIAN_BLOOD_COST = 1` flat per tick; second resource scales as `int(cuberoot(aether_density))`, defaults to `STONE`
- `INITIAL_STOCKPILE` tiers: Common (80): stone, water, wood, soft_rock, hard_rock; Uncommon (40): iron, copper, meat, blood, aether_crystals; Rare (15): rare_metals; Trace (5): aetherite
- `CONSUMABLE_RESOURCES` = all resources except KNOWLEDGE (categorised as STATIC)

### Files in Project Root

```
.gitignore         — local ignore rules
README.md          — project overview and usage
AGENTS.md          — assistant/agent notes
pyproject.toml     — packaging and dev tooling metadata
worldengine.py     — game entrypoint
out.gv / out.png   — architecture diagram artifacts
```

---

## 2. Current State Assessment

### 2.1 What Works Well

- **Procedural generation is functional.** `generate_dungeon_world()` produces 3 dungeon levels and 10 outside zones.
- **Initial zone event system exists.** The code now tracks 3 initial Tier 1 zones and accumulates event progress on repeated expeditions.
- **Save/load is stable.** Transactional save writes and v1→v2 migration support are present.
- **REPL commands are implemented.** `oracle.py` supports hero dispatch, zone listing, and save selection.
- **Domain test coverage exists.** `tests/test_smoke.py` covers generation, serialization, save/load, expedition flow, and the new event behavior.
- **Expedition cost system implemented.** Sending a hero on expedition now costs `expedition_supplies` + stockpile resources (`WOOD`, `FIBRE`, `MEAT`, `WATER`). Zone pressure escalates exponentially per turn with jittered damage. Harvest scales logarithmically with duration.
- **Guardian per-tick maintenance implemented.** Each guardian assigned to a level pays 1 blood/tick (flat) plus a level-scaled resource (default `STONE`, cost = `int(cuberoot(aether_density))`) each tick. Dead or unassigned guardians are skipped.
- **Initial stockpile seeded on new worlds.** New games start with tiered resources (80/40/15/5). Knowledge categorised as STATIC (not shown in stockpile display). Harvest multiplier bumped to 0.5 for ~2–4 wood per expedition turn.
- **Aether crystal growth system implemented.** Each dungeon level has a set of aether crystal nodes (2/3/4 for levels 1/2/3) that grow at `level` crystals/tick up to a per-node cap (5/7/10). `harvest <level_id>` extracts all node contents into stockpile. `nodes <level_id>` displays node details. Nodes shown in level summary and specific level view.

### 2.2 Remaining Issues

- `WorldZone` event handling is currently a one-shot encounter; a broader event system is not yet extracted into its own module.
- Resource distribution across zones and levels is still ad hoc and marked by TODO comments in `generation.py`.
- There is no `LICENSE` file in the repository.
- There is no CI workflow configured.
- Tests are still concentrated in a single smoke test module; coverage should be expanded to isolated unit tests.
- `DungeonWorld` and `entities.py` are still monolithic; future refactoring should split domain concerns for maintainability.

### 2.3 Code Quality

| Dimension | Assessment |
|---|---|
| Readability | Good for current scale; `entities.py` is large and could benefit from decomposition |
| Naming | Mostly clear; some internal comments remain outdated |
| Docstrings | Present for many methods, but not exhaustive |
| Type hints | Widely used, but not uniformly enforced across all methods |
| Error handling | Adequate for user input and save I/O, weaker in gameplay state transitions |
| TODOs | Resource distribution and event expansion are explicit pending work |

### 2.4 Test Coverage

Current tests validate major world generation and event flow paths but do not cover:
- edge cases around save migration failures
- multiple expedition interactions
- resurrection/death state transitions
- builder lifecycle behavior

### 2.5 Technical Debt

| Item | File | Severity |
|---|---|---|
| Event system not extracted | `entities.py` | Medium |
| Resource distribution TODOs | `generation.py` | Low/Medium |
| No CI workflow | repository root | Medium |
| No LICENSE | repository root | Medium |
| Limited test granularity | `tests/` | Medium |
| Monolithic core file | `entities.py` | Medium |

### 2.6 Project Files

| File | Present? |
|---|---|
| `.gitignore` | Yes |
| `README.md` | Yes |
| `AGENTS.md` | Yes |
| `LICENSE` | No |
| `pyproject.toml` | Yes |
| CI config | No |
| Test config | No |

---

## 3. Roadmap

### Next Days

1. **Add a LICENSE file.** A simple MIT license is the best low-friction choice for an open project.
2. **Add CI coverage.** Start with a GitHub Actions workflow that runs `python -m unittest` and optionally `python -m py_compile`.
3. ~~**Refresh documentation.** Update `README.md` and `AGENTS.md` to match the current command set, world loading flow, and domain API.~~ ✅ Done
4. ~~**Remove or implement `display_world_zones()`.** Either provide zone detail output or remove the placeholder entirely.~~ ✅ Done
5. **Clean up stale comments/TODOs.** Focus first on resource generation comments and domain API notes in `generation.py` and `entities.py`.
6. **Write full resource descriptions.** Expand `RESOURCE_DESCRIPTIONS` in `constants.py` with origin and use notes for all resources. (Deferred — player to write)
7. **Balance hero, builder, and guardian costs.** Review and adjust `HERO_COSTS` and add missing cost tables for builders and guardians across all resources.

### Next Weeks

1. ~~**Implement tick-phase game logic.** Replace `_process_environmental_events()` and `_process_unit_statuses()` with real hazards, recovery, and status updates.~~ ✅ Done (env events dispatches creature encounters; unit status applies builder decay and per-tick effects)
2. **Expand test coverage.** Add focused tests for generation rules, serialization round-trips, save migration, and expedition edge cases.
3. **Normalize naming and type use.** Ensure naming conventions are consistent across levels, guardians, and expedition state, and widen type hint coverage in the domain layer.
4. **Strengthen save/load validation.** Add tests and safeguards for corrupted save data and invalid migration inputs.
5. **Harden the CLI flow.** Verify command parsing and error messages across the `oracle.py` command set.

### Next Months

1. **Formalize the resource economy.** Define which resources belong to dungeon levels versus outside zones and begin a crafting/refining system.
2. **Add specialization effects.** Make hero specializations meaningfully affect expedition loot, survival, and return rates.
3. **Introduce wider unit systems.** Add builder task progress, guardian assignments, and deeper hero progression mechanics.
4. **Modularize domain code.** Consider splitting `entities.py` into more focused modules such as `units.py`, `expeditions.py`, and `resources.py` once the core rules stabilize.
5. **Add more tests and linting.** Use `pyproject.toml` to enable `pytest` and `mypy` or linting in CI.

### Next Years

1. **Turn this prototype into a fully playable experience.** Expand the current domain into a richer game loop with deeper persistent progression.
2. **Add a more polished interface.** Once core systems are stable, build a better terminal UI or a minimal graphical frontend.
3. **Establish release hygiene.** Add CI, packaging metadata, contribution documentation, and a LICENSE file.
4. **Extend the unit ecosystem.** Add more meaningful builder, guardian, and hero specialization gameplay, including distinct roles and task assignments.
5. **Grow the resource and crafting system.** Implement resource refinement, recipes, and more distinct item flows between zones and the dungeon.

---

## Appendix: Bug Impact Matrix

| Bug | Blocks new game? | Blocks loading saves? | Blocks playing? | Runtime crash? |
|---|---|---|---|---|
| Stale Resource refs in generation.py | **Yes** | No | Yes | Yes (AttributeError) |
| `guardian_power` vs `guardian_power_level` in display.py | No | No | Conditional | Yes (if player runs `random`) |
| `Scholar` removed from specializations | No | No | No | No (silent dead path) |
| No tests | No | No | No | No — but every fix is blind |
