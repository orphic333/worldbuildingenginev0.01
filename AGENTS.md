# AGENTS.md — Worldbuilding Engine

## Entrypoints

```bash
python worldengine.py               # thin wrapper → main()
python -m worldbuildingengine.main  # direct
python -m unittest tests/test_smoke.py  # 21 smoke tests
```

## Architecture

```
worldengine.py         ← thin wrapper
worldbuildingengine/
├── main.py            # Startup: world select → generate/load → oracle
├── oracle.py          # REPL command dispatch (process_user_command)
├── entities.py        # ALL entity classes (BaseUnit, Hero, Guardian, Builder,
│                      #   Expedition, DungeonLevel, WorldZone, DungeonWorld)
├── generation.py      # Level & zone generation
├── save_load.py       # JSON persistence (transactional: .tmp + os.replace)
├── migrations.py      # Schema migration pipeline (v1→v2)
├── display.py         # Terminal output helpers
├── recruitment.py     # Unit creation flows
├── constants.py       # Resource enum (22 members), specializations, word lists
└── types.py           # Type aliases (forward-refs to avoid circular imports)
saves/                 # JSON save files
tests/test_smoke.py    # unittest smoke tests
```

**Critical constraint:** `entities.py` keeps all classes in one file to avoid circular imports (`Expedition` ↔ `DungeonWorld` ↔ `Hero` ↔ `WorldZone` all cross-reference).

## Known Bugs (game is partially broken)

| Bug | File | Effect |
|---|---|---|
| Stale `Resource` enum refs | `generation.py:48-106` | Blocks new world generation (`AttributeError`) — old names `RAW_AETHER`, `OBSIDIAN`, `SHADOW_MATTER` deleted |
| Wrong attr name `guardian_power` | `display.py:86` | Crashes on `random` command — should be `guardian_power_level` |
| `"Scholar"` no longer in specializations | `entities.py:284-285` | KNOWLEDGE double-harvest is dead code — should check `"Researcher"` |

**Fix order:** patch `constants.py` → `generation.py` → `display.py` → `entities.py`, then run tests.

## Oracle Commands

| Command | Action |
|---|---|
| `<N>` | View dungeon level N (1–3, hardcoded) |
| `random` | Random level |
| `recruit` | Create unit (hero/guardian/builder) |
| `heroes` | List ALL units by type |
| `hero <id>` | Unit detail (heroes only) |
| `zones` | List discovered zones |
| `send <hid> <zid> <dur>` | Dispatch hero on expedition |
| `expeditions` | Active expedition status |
| `tick` | Advance one turn (auto-saves) |
| `stockpile` | Show accumulated resources |
| `save` | Save to JSON |
| `exit` | Save + quit |

## Serialization

- All data classes implement `to_dict()` / `from_dict()`.
- `Resource` enum serialized via `.value` strings, reconstructed with `Resource(k)`.
- Expeditions serialized as metadata only (hero/zone refs by ID, rehydrated on load).
- Save files get `schema_version` (currently `2` from `migrations.py`).
- Old flat-format saves (`"Level N"` keys) migrated via `migrations.migrate_v1_to_v2`.
- Transactional writes: write to `.tmp`, then `os.replace()`.

## Key Facts

- **stdlib only:** `json`, `random`, `os`, `enum`. No `requirements.txt` or `pyproject.toml`.
- **`DungeonWorld`** owns `heroes`, `guardians`, `builders`, `stockpile`, `turn`, `next_unit_id`.
- **Researcher** specialization doubles `KNOWLEDGE` harvest (but see bug above — checks `"Scholar"` instead).
- **Zones deplete** on harvest (`_resolve` subtracts from `resource_nodes`).
- **No type hints** anywhere in the codebase (except `types.py` type aliases).
- **`mypy.ini`** exists but mypy does not ship wheels for Python 3.14 — type checking is currently impossible.
- **`_test_roundtrip.json`** may be left behind in `saves/` after running tests — safe to delete.
- `MAX_LEVEL = 3` only affects new worlds. Loaded saves preserve their own structure.
