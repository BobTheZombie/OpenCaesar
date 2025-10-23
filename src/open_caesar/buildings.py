"""Definitions for the building types in OpenCaesar."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pygame


@dataclass(frozen=True)
class BuildingType:
    """Represents a structure the player can place in the city."""

    name: str
    cost: int
    color: pygame.Color
    description: str
    food_delta: int = 0
    population_delta: int = 0
    revenue: int = 0


BUILDINGS: Dict[str, BuildingType] = {
    "road": BuildingType(
        name="Road",
        cost=5,
        color=pygame.Color(110, 92, 65),
        description="Connects structures and improves movement.",
    ),
    "house": BuildingType(
        name="Insula",
        cost=25,
        color=pygame.Color(214, 189, 129),
        description="Provides housing for new citizens.",
        population_delta=8,
    ),
    "farm": BuildingType(
        name="Farm",
        cost=40,
        color=pygame.Color(141, 174, 97),
        description="Produces food for the population.",
        food_delta=12,
    ),
    "market": BuildingType(
        name="Market",
        cost=60,
        color=pygame.Color(196, 166, 92),
        description="Generates tax revenue while consuming food.",
        food_delta=-6,
        revenue=18,
    ),
    "well": BuildingType(
        name="Well",
        cost=20,
        color=pygame.Color(88, 146, 173),
        description="Improves desirability but has no direct effects yet.",
    ),
}

BUILDING_ORDER = list(BUILDINGS.keys())

