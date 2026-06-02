# Worldbuilding Engine v0.01

A terminal-based dungeon management simulation with adventure, lore and high stakes that pushes the creativity of players to the limit.

## Overview

Procedurally generates a 3-level expandable dungeon ("The Great Descent") with unique level names, aether density, and guardian power levels. Dive into an interactive oracle system to explore your dungeon, recruit heroes, prepare for expedition simulation and perform managerial tasks.

## Features

- **Procedural Dungeon Generation** — 3 unique levels
- **Oracle Terminal** — Query levels by number, navigate the dungeon, issue commands to units, manage and grow the dungeon as a whole
- **Save/Load System** — Persist dungeon worlds and world information as JSON files
- **Unit Management** — Recruit heroes and other units with distinct specializations and track their stats.

## Getting Started

```bash
python worldengine.py
```

Select an existing world or create a new one at startup.

### Oracle Commands

| Command       | Action |
|---------------|---|
| `<number>`    | View a specific level (1–100) |
| `random`      | Discover a random level |
| `recruit`     | Create a new hero |
| `heroes`      | List all heroes |
| `hero <id>`   | View detailed hero status |
| `zones`       | View information on discovered zones outside the dungeon|
| `expeditions` | See the status of ongoing expeditions, completed ones, and initiate expeditions|
| `stockpile`   | View the stockpile of your dungeon which contains amassed resources and knowledge|
| `tick`        | Move the game forward by one tick|
| `save`        | Save your game|
| `exit`        | Quit the oracle |

### Hero Specializations

| Class           | Role                                                                       |
|-----------------|----------------------------------------------------------------------------|
| **Prospector**  | Detects resource hotspots during expeditions and mines them efficiently    |
| **Researcher**  | Gathers knowledge in zones and performs research to unlock crafting recipes|
| **Adventurer**  | All-rounder with logistics skills; excels at leading hyper-specific goals  |
| **Scout**       | Scouts zones to reveal risks, rewards, and enables long-term planning      |
| **Warrior**     | Combat specialist; clears enemies and defends expedition parties           |

## Project Structure

```
worldengine.py                     — Thin wrapper (delegates to package)
worldbuildingengine/
├── __init__.py                    — Package marker
├── main.py                        — Startup flow (world selection, main loop)
├── oracle.py                      — REPL command dispatch
├── entities.py                    — All entity classes
├── generation.py                  — Procedural level and zone generation
├── constants.py                   — Resource enum, word lists, specializations
├── save_load.py                   — JSON persistence (transactional saves)
├── migrations.py                  — Schema version migration pipeline
├── display.py                     — Terminal output helpers
├── recruitment.py                 — Unit creation flows
├── types.py                       — Type aliases
saves/                             — Saved dungeon worlds (JSON)
tests/
├── __init__.py
└── test_smoke.py                  — 21 smoke tests
mypy.ini                           — Type-checking config (Python 3.14+)
```

## Roadmap

- Hero expedition simulation with danger ratings on zones
- Resource extraction and crafting system
- Hero injury, sanity, and stamina degradation mechanics
- Procedural events and hazards during ticks
- Notoriety scale
