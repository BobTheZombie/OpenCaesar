"""Core city simulation logic."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, List, Optional, Tuple

import pygame

from .buildings import BUILDINGS
from .constants import GRID_COLS, GRID_ROWS, TILE_SIZE

GridPosition = Tuple[int, int]


@dataclass
class City:
    """Represents the city state and contains the simulation rules."""

    treasury: int = 400
    food: int = 40
    population: int = 20
    happiness: int = 55
    grid: List[List[Optional[str]]] = field(
        default_factory=lambda: [[None for _ in range(GRID_ROWS)] for _ in range(GRID_COLS)]
    )
    history: Deque[str] = field(default_factory=lambda: deque(maxlen=100))

    def can_place(self, building_key: str, pos: GridPosition) -> bool:
        """Return True when a building may be placed at the given position."""

        col, row = pos
        if not (0 <= col < GRID_COLS and 0 <= row < GRID_ROWS):
            return False
        if self.grid[col][row] is not None:
            return False
        return self.treasury >= BUILDINGS[building_key].cost

    def place(self, building_key: str, pos: GridPosition) -> bool:
        """Attempt to place a building on the grid."""

        if not self.can_place(building_key, pos):
            return False

        building = BUILDINGS[building_key]
        col, row = pos
        self.grid[col][row] = building_key
        self.treasury -= building.cost
        self.history.append(f"Placed {building.name} at {pos}")
        return True

    def demolish(self, pos: GridPosition) -> bool:
        """Remove a building from the grid."""

        col, row = pos
        if not (0 <= col < GRID_COLS and 0 <= row < GRID_ROWS):
            return False
        if self.grid[col][row] is None:
            return False
        building_key = self.grid[col][row]
        self.grid[col][row] = None
        if building_key:
            building = BUILDINGS[building_key]
            refund = max(0, building.cost // 2)
            self.treasury += refund
            self.history.append(f"Demolished {building.name} at {pos}, refunded {refund} denarii")
        return True

    def iterate(self) -> None:
        """Progress the simulation by one tick."""

        food_delta = 0
        population_delta = 0
        revenue = 0

        for col in range(GRID_COLS):
            for row in range(GRID_ROWS):
                key = self.grid[col][row]
                if key is None:
                    continue
                building = BUILDINGS[key]
                food_delta += building.food_delta
                population_delta += building.population_delta
                revenue += building.revenue

        # Apply changes with mild balancing to avoid runaway growth.
        self.food = max(0, self.food + food_delta)
        self.population = max(0, self.population + population_delta)
        self.treasury += revenue

        # Adjust happiness based on abundance.
        happiness_change = 0
        if self.food >= self.population:
            happiness_change += 1
        else:
            happiness_change -= 1
        if revenue > 0:
            happiness_change += 1

        self.happiness = max(0, min(100, self.happiness + happiness_change))

        summary = (
            f"Tick: +{revenue} denarii, food Δ {food_delta}, population Δ {population_delta}, "
            f"happiness now {self.happiness}"
        )
        self.history.append(summary)

    def tile_at_pixel(self, pixel: Tuple[int, int]) -> Optional[GridPosition]:
        """Convert pixel coordinates to grid coordinates."""

        x, y = pixel
        col = x // TILE_SIZE
        row = y // TILE_SIZE
        if 0 <= col < GRID_COLS and 0 <= row < GRID_ROWS:
            return col, row
        return None

    def count_buildings(self) -> Dict[str, int]:
        """Return counts of the currently placed buildings."""

        counts: Dict[str, int] = {key: 0 for key in BUILDINGS}
        for column in self.grid:
            for key in column:
                if key:
                    counts[key] += 1
        return counts


def grid_rect(col: int, row: int) -> pygame.Rect:
    """Return the rectangle representing the tile in pixel coordinates."""

    from .constants import TILE_SIZE

    return pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

