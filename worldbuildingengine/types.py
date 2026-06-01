"""Type aliases for the worldbuildingengine package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .constants import Resource

if TYPE_CHECKING:
    from .entities import (
        Hero, Guardian, Builder,
        DungeonLevel, WorldZone, Expedition,
    )

ResourceDict = dict[Resource, int]
HeroList = list[Hero]
GuardianList = list[Guardian]
BuilderList = list[Builder]
LevelDict = dict[int, DungeonLevel]
ZoneDict = dict[int, WorldZone]
ExpeditionList = list[Expedition]
SaveDict = dict  # JSON-deserialized dict, too dynamic to pin

LootDict = dict[Resource, int]
InventoryDict = dict[Resource, int]
