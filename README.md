# Worldbuilding Engine v0.01

A terminal-based dungeon management simulation with a procedural dungeon, expedition mechanics, and persistent JSON world saves.

## Overview

The game generates a 3-level dungeon and a set of outside world zones. Players recruit heroes and builders, send heroes on expeditions to discover resources, and manage the dungeon stockpile through a turn-based oracle command system.

## Features

- **Procedural Dungeon Generation** — Generates 3 dungeon levels and 10 outside zones.
- **Oracle Command Interface** — Interact with the game through a text-based command loop.
- **Save/Load System** — Persist world state safely to JSON files.
- **Unit Management** — Recruit heroes and builders and track hero stats during expeditions.
- **Expedition Lifecycle** — Send heroes to zones, resolve loot, and update stockpile on tick.

## Getting Started

```bash
python worldengine.py
```

At startup, choose to load an existing world or create a new one.

### Commands

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
| `stockpile` | View current stockpile resources |
| `save` | Save the current world |
| `exit` | Save and quit |

### Hero Specializations

| Class | Role |
|---|---|
| `Prospector` | Efficient at extracting resources during expeditions |
| `Researcher` | Doubles `KNOWLEDGE` harvest from zones |
| `Adventurer` | Generalist hero with balanced progression |
| `Scout` | Good at scouting and risk assessment |
| `Warrior` | Strong in combat-oriented expedition challenges |

## Running Tests

```bash
python -m unittest tests/test_smoke.py
```

## Project Structure

```
worldengine.py
worldbuildingengine/
├── main.py
├── oracle.py
├── entities.py
├── generation.py
├── constants.py
├── save_load.py
├── migrations.py
├── display.py
├── recruitment.py
└── types.py
tests/
├── __init__.py
└── test_smoke.py
pyproject.toml
```

## Notes

- Builders are created with IDs only; they no longer require a name.
- `Researcher` specialization currently doubles `KNOWLEDGE` harvest during expeditions.
- `display_world_zone()` is still a placeholder function in `display.py`.
- There is currently no CI workflow or LICENSE file in the repository.
