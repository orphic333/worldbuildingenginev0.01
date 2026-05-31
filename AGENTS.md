# AGENTS.md — Worldbuilding Engine

## Entrypoints

```bash
python worldengine.py                  # thin wrapper
python -m worldbuildingengine.main    # direct
```

## Architecture

```
worldbuildingengine/
├── constants.py    # Resource enum, word lists, specializations
├── entities.py     # All entity classes (BaseUnit, Hero, Guardian, Builder,
│                   #   Expedition, DungeonLevel, WorldZone, DungeonWorld)
├── generation.py   # Level + zone generation
├── save_load.py    # JSON persistence (saves/ directory)
├── display.py      # Terminal output helpers
├── recruitment.py  # Unit creation flows
├── oracle.py       # Command dispatch + REPL loop
└── main.py         # Startup flow (initialize_world, main)
```

Key rule: entities.py keeps all classes in one file to avoid circular imports (Expedition, DungeonWorld, Hero, WorldZone all cross-reference).

## Serialization

- All data classes (`DungeonLevel`, `WorldZone`, `DungeonWorld`) use `to_dict()` / `from_dict()` pattern.
- `Resource` enum (in `constants.py`) uses `.value` strings in JSON, reconstructed via `Resource(k)` on load.
- `DungeonWorld.active_expeditions` serializes metadata only — not fully rehydrated on load.
- Old-format saves (flat `"Level N"` keys) handled by backward compat in `save_load.py`.

## Oracle Commands

| Command | Action |
|---|---|
| `<N>` | View dungeon level N (1–3) |
| `random` | Random level |
| `recruit` | Create unit (hero/guardian/builder) |
| `heroes` | List all units by type |
| `hero <id>` | Unit detail |
| `zones` | List discovered zones |
| `send <hid> <zid> <dur>` | Dispatch hero on expedition |
| `expeditions` | Active expedition status |
| `tick` | Advance one turn (increments turn, processes expeditions, stubs for events/status) |
| `stockpile` | Show accumulated resources |
| `exit` | Quit |

## No External Dependencies

stdlib only: `json`, `random`, `os`, `enum`. No requirements.txt, no pyproject.toml, no virtualenv needed.

## Resource Economy Notes

- `Resource` enum has 22 members — all resources explicitly defined in AGENTS.md task notes.
- Zones are depleted on harvest (expedition `_resolve` subtracts from `resource_nodes`).
- Stockpile accumulates across expeditions; persists in save JSON.
- Scholar specialization doubles `KNOWLEDGE` harvest.

## Save Files

- Stored as JSON in `saves/` relative to CWD.
- Level count (`MAX_LEVEL = 3`) only affects new world generation. Loaded saves keep their original structure.
