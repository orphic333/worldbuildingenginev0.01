# Worldbuilding Engine v0.01

A terminal-based dungeon world generator and hero management simulation.

## Overview

Procedurally generates a 100-level dungeon ("The Great Descent") with unique level names, aether density, and guardian power levels. Dive into an interactive oracle system to explore your dungeon, recruit heroes, and prepare for expedition simulation.

## Features

- **Procedural Dungeon Generation** — 100 unique levels with scaling difficulty
- **Oracle Terminal** — Query levels by number, discover random floors, navigate the dungeon
- **Save/Load System** — Persist dungeon worlds as JSON files
- **Hero Management** — Recruit heroes with distinct specializations and track their stats

## Getting Started

```bash
python worldengine.py
```

Select an existing world or create a new one at startup.

### Oracle Commands

| Command | Action |
|---|---|
| `<number>` | View a specific level (1–100) |
| `random` | Discover a random level |
| `recruit` | Create a new hero |
| `heroes` | List all heroes |
| `hero <id>` | View detailed hero status |
| `exit` | Quit the oracle |

### Hero Specializations

| Class | Role |
|---|---|
| **Prospector** | Extracts raw resources from the depths |
| **Scholar** | Seeks ancient knowledge hidden in the dark |
| **Warder** | Endures the dangers of deep descents |

## Project Structure

```
worldengine.py      — Main application entry point
world_data.json     — Pre-generated dungeon world data
engine_flowchart.*  — System architecture diagrams
worldengine_flow.*  — Program flow diagrams
saves/              — Saved dungeon worlds (JSON)
```

## Roadmap

- Hero expedition simulation with delve danger scaling
- Resource extraction and crafting system
- Hero injury, sanity, and stamina degradation mechanics
- Procedural events and hazards during descents
