# ROADMAP.md — Worldbuilding Engine v0.01

> Analysis date: 2026-06-16
> Based on current repository state and implemented code changes.

---

## 1. Codebase Overview

### Purpose

A terminal-based dungeon management simulation. The player runs a dungeon, recruits units (heroes, guardians, builders), dispatches heroes to explore outside-world zones, extracts resources, and accumulates a stockpile. The game is turn-based (`tick`) with an interactive REPL ("the Oracle").

### Intended Users

Solo player / game dev prototyping. Not yet a released game.

### Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Persistence | JSON files in `saves/` directory |
| Concurrency | None (single-threaded) |
| Testing | Existing smoke tests in `tests/test_smoke.py` |
| Packaging | Flat package (`worldbuildingengine/`) with `pyproject.toml` |

No runtime dependencies. `pyproject.toml` defines dev extras for test and type-check tooling.

### Architecture

```
worldengine.py  (thin wrapper)
  └── worldbuildingengine/
        ├── main.py         — Startup flow (world selection, create/load)
        ├── oracle.py       — REPL command dispatch loop
        ├── entities.py     — Core domain model and game state
        ├── generation.py   — Procedural generation of levels + zones
        ├── save_load.py    — JSON persistence with transactional writes
        ├── migrations.py   — Schema migration pipeline (v1 → v2)
        ├── display.py      — Terminal output helpers
        ├── recruitment.py  — Unit creation flows
        ├── constants.py    — Resource enum, word lists, specializations
        └── tests/          — smoke tests and future unit tests
```

**Design pattern:** Thin CLI layer in `oracle.py` and `recruitment.py` delegates game logic to the domain model in `entities.py`. State objects serialize via `to_dict()` / `from_dict()`.

**Key architectural decisions:**
- `DungeonWorld` is the central state container holding levels, zones, units, expeditions, stockpile, and turn state.
- `entities.py` contains all core entities to avoid circular import issues between `DungeonWorld`, `Hero`, `WorldZone`, and `Expedition`.
- Save schema versioning is implemented in `migrations.py`, and transactional save writes are implemented in `save_load.py`.

### Entity Relationships (Simplified)

```
DungeonWorld
 ├── levels: dict[int, DungeonLevel]
 │     └── resource_nodes: dict[Resource, int]
 ├── zones: dict[int, WorldZone]
 │     └── resource_nodes: dict[Resource, int]
 ├── heroes: list[Hero]
 ├── guardians: list[Guardian]
 ├── builders: list[Builder]
 ├── active_expeditions: list[Expedition]
 │     └── hero → Hero
 │     └── target_zone → WorldZone
 │     └── world → DungeonWorld
 ├── stockpile: dict[Resource, int]
 └── turn: int
```

### Entry Points

| Command | Effect |
|---|---|
| `python worldengine.py` | Runs thin wrapper |
| `python -m worldbuildingengine.main` | Direct invocation |

### Notable Config

- `SAVE_FOLDER = "saves"` — relative to CWD
- `MAX_LEVEL = 3` — number of initially generated dungeon levels
- `CURRENT_SCHEMA_VERSION = 2` in `migrations.py`

### Files in Project Root

```
.gitignore         — Blocks __pycache__, .venv, .idea, saves
README.md          — Project overview and commands
AGENTS.md          — Agent notes, refreshed
pyproject.toml     — Packaging and dev tooling metadata
worldengine.py     — Thin wrapper to start the game
out.gv / out.png   — Generated architecture/diagram artifacts
```

---

## 2. Current State Assessment

### 2.1 What Works Well

- **Procedural generation is functional.** `generate_dungeon_world()` now uses the current `Resource` enum and reliably creates 3 dungeon levels and 10 outside zones.
- **Save/load persistence is stable.** The project persists world state transactionally and supports schema upgrades via `migrate_data()`.
- **Domain API exists.** `DungeonWorld` exposes `create_hero()`, `create_builder()`, `send_hero_on_expedition()`, and `advance_turn()` for gameplay flows.
- **REPL command handling is implemented.** `oracle.py` supports saving, recruiting, sending heroes, listing zones, and showing stockpile state.
- **Smoke tests are present.** `tests/test_smoke.py` validates generation, serialization round-trips, save/load, display helpers, and expedition lifecycle.
- **Packaging metadata exists.** `pyproject.toml` is present with development dependencies declared.

### 2.2 Remaining Issues

- (Resolved) `display_world_zones()` in `display.py` has been implemented and shows known zone details.
- Turn-processing phases `_process_environmental_events()` and `_process_unit_statuses()` remain unimplemented placeholders.

> #### `_process_environmental_events()` — Design Reference
> *Entry: 2026-06-19*
>
> **Purpose:** Generate and apply world, dungeon, and expedition events that make the game world feel reactive and resistant to the player. Events challenge the player's plans — discoveries, hazards, delays, encounters.
>
> **Design notes:**
> - Events should be varied in scope: expedition events (discovery, hazard, encounter), dungeon events (aether fluctuation, structural issues), and world events (seasonal, regional phenomena).
> - Some events are instantaneous, others are persistent with duration (counted in turns). `DungeonLevel.active_events` is already available for persistent events.
> - `WorldZone.threat_level` should influence event probability for zone-linked events.
> - Events should create meaningful tradeoffs, not just random noise.
>
> **Short-term plan:** Keep the hook in `entities.py` but wire it to roll for world and expedition events each tick, apply/expire persistent events, and print event messages.
>
> **Long-term plan:** Extract event logic into `events.py` with dedicated data types (`GameEvent`, `EventOutcome`) when complexity grows.

> #### `_process_unit_statuses()` — Design Reference
> *Entry: 2026-06-19*
>
> **Purpose:** Update vitals and other stats for all unit types (heroes, guardians, builders, and future units) on each tick. Works hand-in-hand with event logic — events may inject modifiers to tick effects.
>
> **Design notes:**
> - Complementary to `_apply_zone_pressure()`: zone pressure damages heroes during active expeditions, unit status handles passive tick-by-tick changes to all units everywhere (idle or busy).
> - Should scale to hundreds or thousands of units. Each unit class should own its tick logic via a method like `apply_tick_effects()` on `BaseUnit`, so `_process_unit_statuses` stays a simple dispatch loop.
> - Builders are not permanent — they gradually erode and die. A `lifespan` field and decay counter in `apply_tick_effects()` models this.
> - Future expansion: passive healing, stamina/sanity recovery while idle, guardian upkeep costs, status effect application/expiry.
>
> **Short-term plan (✅ Done 2026-06-19):** Builder decay implemented. `apply_tick_effects()` added to `BaseUnit` (no-op default). `Builder` overrides it to decrement `lifespan` by 1 every 2 ticks, marking dead when expired. `_process_unit_statuses` now dispatches to all units.
>
> **Long-term plan:** Extract into `statuses.py` or `tick_effects.py` with registration-based hooks when complexity grows.

- Some in-code TODOs and comments indicate resource distribution and hero inventory systems are still draft-level.
- (Resolved) Documentation files (`AGENTS.md`, `README.md`) have been refreshed to match current commands and domain behavior.
- There is no LICENSE file in the repository.
- There is no CI workflow configured yet.
- Test coverage is limited to a single smoke test module.

### 2.3 Code Quality

| Dimension | Assessment |
|---|---|
| Readability | Good — modular files and clear sectioning |
| Naming | Generally good, but a few inconsistencies remain in comments and helper naming |
| Docstrings | Present for most functions, with a few placeholder notes |
| Type hints | Present in many functions and classes, though not uniformly enforced |
| Error handling | Present in save/load and command parsing, but still minimal in gameplay flows |
| Dead code | Some stub methods and in-code TODO comments remain |

### 2.4 Test Coverage

Existing tests are a strong start, but they are currently limited to smoke-style coverage in `tests/test_smoke.py`. The project would benefit from additional unit tests around domain rules, save migration, and edge cases.

### 2.5 Security Surface

| Risk | Location | Severity |
|---|---|---|
| `json.load()` on untrusted save files | `save_load.py` | Low |
| `input()` calls in REPL | `oracle.py`, `recruitment.py`, `main.py` | None for local use |
| Save directory listing | `save_load.py` | Low |

No network, no external I/O beyond local save files, and no shell execution vectors.

### 2.6 Performance

Not a concern for the current scale. World generation and turn updates operate over at most a handful of entities and zones.

### 2.7 Technical Debt

| Item | File | Severity |
|---|---|---|
| (Resolved) Empty display stub | `display.py` | — |
| Tick-phase stubs | `entities.py` | Medium |
| (Resolved) Stale documentation | `AGENTS.md`, `README.md` | — |
| No LICENSE | repository root | Medium |
| No CI workflow | repository root | Medium |
| Limited test coverage | `tests/` | Medium |
| Resource system TODOs | `generation.py`, `entities.py` | Medium |

### 2.8 Project Files

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

### Next Weeks

1. **Implement tick-phase game logic.** Replace `_process_environmental_events()` and `_process_unit_statuses()` with real hazards, recovery, and status updates.
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
