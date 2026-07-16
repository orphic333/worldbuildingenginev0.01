# ROADMAP.md — Worldbuilding Engine v0.01

> Analysis date: 2026-07-12 
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

## 3. Structured Implementation Phases

### Phase 1: Terminal Screen Engine & Navigation (2–3 Hours)
* **Goal:** Transition from a scrolling command-line REPL to a multi-screen terminal dashboard.
* **Core Actions:**
  - Create a custom terminal frame rendering engine (`ScreenManager` in `display.py`) using raw ANSI escape codes.
  - Implement Windows-compatible Virtual Terminal Processing setup via `ctypes` at launch.
  - Support instant screen navigation via keyboard keypresses (e.g., `D` for Dungeon, `Z` for Zone Map, `S` for Stockpile, `A` for Advisors).
* **Rationale:** Establishes crucial UI infrastructure, preventing flickering/scrolling and enabling complex drawing interfaces.

### Phase 2: Eldritch Title Screen & Procedural Dungeon Map (6–8 Hours)
* **Goal:** Elevate player first impression and generate procedurally unique dungeon levels.
* **Core Actions:**
  - Build an animated splash screen cycling rotating cryptic symbols/runes via standard library timers.
  - Upgrade dungeon generation to procedurally map out walls, corridors, rooms, and aether nodes onto 2D ASCII grids using the world's name or a unique ID as a seed.
  - Animate active units (builders, researchers, miners) as color-coded symbols moving within the map.
  - Expand level cap from 3 to 15.
* **Rationale:** Delivers the primary thematic atmosphere (eldritch/cryptic) and visual dungeon simulation.

### Phase 3: Outside Zone Map & Expedition Viewer (8–10 Hours)
* **Goal:** Visualise world exploration and unit actions in outside regions.
* **Core Actions:**
  - Generate a regional world map layout mapping known and unknown zones.
  - Apply fog of war, distinct color bounds, and background wind/aether hazard animations.
  - Show active expedition paths and zoom-in views tracking individual unit dots (warriors, scouts, researchers) traversing zone grids.
* **Rationale:** Replaces scrolling logs with clear spatial context and real-time visual progress.

### Phase 4: Dynamic Stockpile & Advisor Intelligence (5–7 Hours)
* **Goal:** Visualise internal logistics and implement contextual strategic guidance.
* **Core Actions:**
  - Divide stockpile into visual cells/bins, animating carrier dots transferring resources back and forth.
  - Format the Advisor Reports screen as virtual sheets/documents summarizing turn activities.
  - Write intelligence logic for Advisor specializations, providing contextual hints and warnings (e.g., resource shortages, maintenance alerts).
* **Rationale:** Implements a living economic simulation and turns abstract logs into structured, strategic gameplay advice.

### Phase 5: Code Architecture & Packaging Hygiene (3–4 Hours)
* **Goal:** Eliminate tech debt and secure the repository layout.
* **Core Actions:**
  - Refactor and decompose the large `entities.py` monolith into focused domain files (e.g., `units.py`, `zones.py`, `world.py`).
  - Add standard MIT licensing file.
  - Configure GitHub Actions CI workflow to run test suites automatically.
* **Rationale:** Prevents circular dependency issues and ensures structural maintainability for advanced gameplay loops.

---

## Appendix: Bug Impact Matrix

| Bug | Blocks new game? | Blocks loading saves? | Blocks playing? | Runtime crash? |
|---|---|---|---|---|
| Stale Resource refs in generation.py | **Yes** | No | Yes | Yes (AttributeError) |
| `guardian_power` vs `guardian_power_level` in display.py | No | No | Conditional | Yes (if player runs `random`) |
| `Scholar` removed from specializations | No | No | No | No (silent dead path) |
| No tests | No | No | No | No — but every fix is blind |

## Vision  
Let me tell you how I envision the game: a player opens the game; a minimalist screen shows up; black background, the name of the game and a cryptic symbol in a pixel-like/ASCII-like fashion, rotating. He loads his save and a screen appears showing his developing dungeon. The dungeon itself has a cryptic design, like the workmanship of some eldritch entity (interesting note: no two player dungeons will ever look the same). The player currently has 15 levels and hundreds of units, builders, researchers, miners and so on. He changes screens and selects one of the many expeditions that are running on a tick/turn-based system for a number of turns. The screen changes and shows him a zoomed out zone. Some parts of the zone are coloured (animated, too) some parts are dark. An indicator rests on a specific portion of the coloured part. The player clicks it and it reveals the units on an expedition. He sees tiny dots of different colours, indicating different unit types moving around, seemingly doing things. He returns to his dungeon's home screen and selects a button that takes him to another screen showing the dungeon's stockpile. Here too, there are little dots seemingly in action, moving around, carrying resources in and out of several sections. He returns to his home screen and clicks another button that selects that takes him to a certain screen where several sheets are before him. Those documents are show information on recent dungeon activities, current dungeon state, internal and external affairs, and so on. Entities called advisors summarise the information for him and reccommend best next actions. This is just a bit of how I'm visualising the end-product, though there's more.

>Date:16/07/2026
###
Added a game details and planning markdown file to track the core of the game and also discussions on game features. 