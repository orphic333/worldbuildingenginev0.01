# ROADMAP.md — Worldbuilding Engine v0.01

> Analysis date: 2026-05-21
> Based on commit `feature/remodularised_files` with post-split edits applied.

---

## 1. Codebase Overview

### Purpose

A terminal-based dungeon management simulation. The player runs a dungeon, recruits units (heroes, guardians, builders), dispatches heroes to explore outside-world zones, extracts resources, and accumulates a stockpile. The game is turn-based (`tick`) with an interactive REPL ("the Oracle").

### Intended Users

Solo player / game dev prototyping. Not yet a released game.

### Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 (stdlib only) |
| Persistence | JSON files in `saves/` directory |
| Concurrency | None (single-threaded) |
| Testing | None |
| Packaging | Flat package (`worldbuildingengine/`) with `worldengine.py` wrapper |

No external dependencies. No `requirements.txt`, `pyproject.toml`, or `setup.cfg`.

### Architecture

```
worldengine.py  (thin wrapper)
  └── worldbuildingengine/
        ├── main.py         — Startup flow (world selection, create/load)
        ├── oracle.py       — REPL command dispatch loop
        ├── entities.py     — All classes (BaseUnit, Hero, Guardian, Builder,
        │                     Expedition, DungeonLevel, WorldZone, DungeonWorld)
        ├── generation.py   — Procedural generation of levels + zones
        ├── save_load.py    — JSON persistence with transactional writes
        ├── migrations.py   — Schema migration pipeline (v1 → v2)
        ├── display.py      — Terminal output helpers
        ├── recruitment.py  — Unit creation flows
        └── constants.py    — Resource enum, word lists, specializations
```

**Design pattern:** Procedural-with-classes hybrid. The command loop (`oracle.py`) reads user input, calls functions in `recruitment.py`, `display.py`, and methods on `DungeonWorld`/`Expedition`. Serialization uses a `to_dict()` / `from_dict()` pattern on all data classes.

**Key architectural decisions (some now stale — see §2):**
- All entity classes live in one `entities.py` to avoid circular imports (Expedition ↔ DungeonWorld ↔ Hero ↔ WorldZone all cross-reference).
- `DungeonWorld` is the central state container. It now owns `heroes`, `guardians`, `builders` lists directly (transitioned from separate lists in `main()`).
- Save schema versioning exists via `migrations.py` (v1 → v2). New `schema_version` key in JSON.

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
- `MAX_LEVEL = 3` — affects new world generation only
- `CURRENT_SCHEMA_VERSION = 2` in `migrations.py`

### Files in Project Root

```
.gitignore         — Blocks __pycache__, .venv, .idea, saves
README.md          — Mostly accurate, stale in places
AGENTS.md          — Out of date, references pre-merge architecture
worldengine.py     — 4-line thin wrapper
out.gv / out.png   — Graphviz diagram (not tracked in git)
```

---

## 2. Current State Assessment

### 2.1 — CRITICAL: The Game is Broken

**`generation.py` references deleted `Resource` enum members.** The `Resource` enum was recently expanded to 22 members (STONE, WOOD, IRON, etc.) but `generation.py` still uses the old names:

| File:Line | Old Name | Status |
|---|---|---|
| `generation.py:48,85,93,102` | `Resource.RAW_AETHER` | **Does not exist** — should be `AETHER_CRYSTALS` or `AETHERITE` |
| `generation.py:51,94,103` | `Resource.OBSIDIAN` | **Does not exist** |
| `generation.py:95,104` | `Resource.SHADOW_MATTER` | **Does not exist** |

**Result:** `create_level_data()` raises `AttributeError` on every call. No new world can be generated. The game is unplayable from a fresh start.

**`display.py:83` uses wrong attribute name:**

```python
# display.py:83 — in display_random_level()
f"Guardian {level_data.guardian_power}"
```

The `DungeonLevel` attribute is `guardian_power_level` (not `guardian_power`). This will crash at runtime if a player runs `random`.

**`entities.py:284-285` Specialization mismatch:**

```python
if (
    resource == Resource.KNOWLEDGE
    and self.hero.specialization == "Scholar"
):
```

`"Scholar"` no longer exists in `SPECIALIZATIONS` (now: `Prospector`, `Researcher`, `Adventurer`, `Scout`, `Warrior`). No hero can ever match this condition, so the KNOWLEDGE double-harvest never triggers.

### 2.2 What Works Well

- **Package split** — The monolithic file was successfully decomposed into 10 modules.
- **Save/load pipeline** — `migrations.py` provides a clean versioned migration framework. The transactional write pattern (write to `.tmp`, then `os.replace`) is production-grade.
- **Modular serialization** — `to_dict()` / `from_dict()` on every data class is consistent and testable.
- **Unit ID system** — `get_next_unit_id()` on `DungeonWorld` is clean.
- **No external dependencies** — stdlib only, zero install friction.

### 2.3 Code Quality

| Dimension | Assessment |
|---|---|
| Readability | Good — consistent indentation, section headers, docstrings |
| Naming | Inconsistent: `guardian_power_level` vs `guardian_power`, `power_level` vs `build_speed` |
| Docstrings | Present on most functions but some are stale ("not yet implemented") |
| Type hints | **None** — no function signatures use Python typing |
| Error handling | Minimal — most I/O errors propagate uncaught to the REPL |
| Dead code | `display.py:117` — empty `display_world_zone()` stub; `save_load.py` imports `DungeonLevel` without using it |

### 2.4 Test Coverage

**Zero.** There are no tests anywhere in the repository. Not a single unit test, integration test, or end-to-end test. This is the highest-risk finding after the bugs in §2.1.

### 2.5 Security Surface

| Risk | Location | Severity |
|---|---|---|
| `json.load()` on untrusted save files | `save_load.py:96` | Low (single-player game) |
| `input()` calls in REPL | `oracle.py`, `recruitment.py`, `main.py` | None (local only) |
| `os.listdir()` without filtering for `.json` | `save_load.py:39` | Low (non-.json files ignored by `.replace()`) |

No exposed secrets, no network, no shell injection vectors.

### 2.6 Performance

Not a concern at this scale. Only 3 levels and 10 zones. The only O(n) concern is depleting resource nodes in `_resolve()`, which iterates a handful of keys.

### 2.7 Technical Debt

| Item | File | Severity |
|---|---|---|
| Stale Resource enum references | `generation.py` | **Critical (blocks all new worlds)** |
| `guardian_power` vs `guardian_power_level` | `display.py:83` | **Critical (crashes on 'random')** |
| `"Scholar"` removed from specializations | `entities.py:285` | **High (dead code path)** |
| Two tick stubs not implemented | `entities.py:647-665` | Medium |
| Unused import (`DungeonLevel`) | `save_load.py:5` | Low |
| Empty stub `display_world_zone()` | `display.py:117` | Low |
| No type hints anywhere | All files | Medium |
| AGENTS.md references old architecture | `AGENTS.md` | Medium |
| README lists old specializations | `README.md` | Low |
| display_world_overview prints 100 levels from old saves | `display.py:58` | Low (old saves still have 100 levels) |

### 2.8 Missing Project Files

| File | Present? |
|---|---|
| `.gitignore` | Yes |
| `README.md` | Yes |
| `AGENTS.md` | Yes (outdated) |
| `LICENSE` | **No** |
| `pyproject.toml` / `setup.cfg` / `setup.py` | **No** (acceptable for this project) |
| CI config | **No** |
| Test config | **No** |

---

## 3. Roadmap

### Immediate (do now — unblocking)

1. **Fix stale `Resource` enum references in `generation.py`**
   - Map `RAW_AETHER` → one or more of `AETHER_CRYSTALS`, `AETHERITE`
   - Map `OBSIDIAN` → probably `STONE`, `HARD_ROCK`, or `RARE_METALS`
   - Map `SHADOW_MATTER` → probably remove or map to one of the 22 real resources
   - Files: `worldbuildingengine/generation.py:48-53,84-106`

2. **Fix `guardian_power` → `guardian_power_level` in `display.py:83`**
   - File: `worldbuildingengine/display.py`, line 83

3. **Fix or remove `"Scholar"` specialization check in `entities.py:284-285`**
   - Either add `"Scholar"` back to `SPECIALIZATIONS` or change the condition to check one of the current specializations (e.g., `"Researcher"` which serves a similar role).
   - File: `worldbuildingengine/entities.py:283-285`

4. **Write a smoke test** before fixing anything else, to catch regressions immediately.
   - A single script that: generates a world → recruits a hero → sends on expedition → ticks → checks stockpile
   - Location: `tests/test_smoke.py`

### Short-term (days to a few weeks)

5. **Normalize naming conventions**
   - Pick one: `guardian_power` vs `guardian_power_level`. Apply everywhere.
   - Pick one: `power` vs `power_level` on Guardian class.
   - Files: `entities.py`, `generation.py`, `display.py`, `oracle.py`

6. **Remove dead code**
   - Delete unused `import DungeonLevel` from `save_load.py`.
   - Delete empty stub `display_world_zone()` from `display.py` or implement it.
   - Remove `is_explored` field entirely from DungeonLevel (it was already removed from `__init__` but `migrations.py:27` still sets it — no-op but misleading).

7. **Reconcile import references with current architecture**
   - `AGENTS.md` still describes `run_oracle_system(world_data, heroes, guardians, builders)` — the signature is now `run_oracle_system(world_data)`.
   - Update the Oracle Commands table and the architecture diagram.

8. **Add type hints** to at least the public function signatures and class `__init__` methods.
   - Start with `constants.py`, `entities.py`, `generation.py`.

9. **Add basic test coverage** for critical paths:
   - `tests/test_generation.py` — generate world, verify 3 levels, 10 zones, first 2 zones discovered
   - `tests/test_serialization.py` — to_dict → from_dict round-trip for each data class
   - `tests/test_resource_harvest.py` — create expedition, verify loot calculation, verify zone depletion
   - `tests/test_migrations.py` — feed v1 flat dict, verify v2 output

10. **Fix `out.gv` / `out.png`** — either track them via git-lfs or add to `.gitignore`.

### Long-term (weeks to months)

11. **Implement the two tick stubs**
    - `_process_environmental_events()` — zone hazards, random events
    - `_process_unit_statuses()` — health/stamina/sanity recovery, starvation, builder task progress
    - Files: `entities.py:647-665`

12. **Build a proper resource integration**
    - The 22-member `Resource` enum is well-defined but disconnected from game mechanics. Current generation only populates 3–4 resources per level/zone.
    - Design which resources drop from dungeon levels vs. outside zones.
    - Implement crafting/refining recipes (`STONE + WOOD → BUILDING_MATERIALS` or similar).
    - Files: `generation.py`, `entities.py` (new crafting module)

13. **Crafting / resource refinement system**
    - Knowledge should unlock recipes.
    - Guardian Cores should be craftable (not naturally occurring).
    - Liquid Aether should require long research.
    - New module: `worldbuildingengine/crafting.py`

14. **Unit specialization gameplay**
    - Each specialization should affect expedition outcomes:
      - `Prospector` → bonus on resource extraction
      - `Researcher` → `KNOWLEDGE` double-harvest (replaces the removed `Scholar`)
      - `Warrior` → reduces zone pressure damage
      - `Scout` → reveals more zone info, lower discover threshold
      - `Adventurer` → generalist bonuses
    - Builder tasks: assign builders to construction, feeding, maintenance
    - Guardian assignment: assign to levels for defense

15. **Expedition expansion**
    - Multiple heroes per expedition (party system).
    - Zone danger should affect hero survival more dynamically.
    - Hero death should cascade (lose all inventory, expedition fails).

16. **Developer experience**
    - Add CI (GitHub Actions): `python -m compileall worldbuildingengine/` at minimum.
    - Add `pyproject.toml` with basic metadata and a `[tool.pytest.ini_options]` section.
    - Create `tests/__init__.py` and `tests/conftest.py` with shared fixtures.
    - Set up `ruff` or `flake8` for linting.
    - Consider adding Python 3.11+ as minimum version and using `enum.StrEnum` for Resource.

17. **Add a LICENSE file** (MIT or GPL-3.0 — project is public on GitHub).

---

## Appendix: Bug Impact Matrix

| Bug | Blocks new game? | Blocks loading saves? | Blocks playing? | Runtime crash? |
|---|---|---|---|---|
| Stale Resource refs in generation.py | **Yes** | No | Yes | Yes (AttributeError) |
| `guardian_power` vs `guardian_power_level` in display.py | No | No | Conditional | Yes (if player runs `random`) |
| `Scholar` removed from specializations | No | No | No | No (silent dead path) |
| No tests | No | No | No | No — but every fix is blind |
