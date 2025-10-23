"""Rendering helpers for the game's user interface."""

from __future__ import annotations

from typing import List

import pygame

from .buildings import BUILDINGS, BUILDING_ORDER
from .city import City, grid_rect
from .constants import (
    COLOR_BACKGROUND,
    COLOR_GRID,
    COLOR_PANEL,
    COLOR_TEXT,
    GRID_COLS,
    GRID_ROWS,
    GRID_WIDTH,
    PANEL_WIDTH,
)


def draw_grid(surface: pygame.Surface, city: City, highlight_pos=None, valid: bool = True) -> None:
    """Draw the map grid and all placed structures."""

    for col in range(GRID_COLS):
        for row in range(GRID_ROWS):
            rect = grid_rect(col, row)
            pygame.draw.rect(surface, COLOR_GRID, rect, 1)
            key = city.grid[col][row]
            if key:
                building = BUILDINGS[key]
                pygame.draw.rect(surface, building.color, rect)

    if highlight_pos is not None:
        from .constants import COLOR_INVALID, COLOR_VALID

        rect = grid_rect(*highlight_pos)
        color = COLOR_VALID if valid else COLOR_INVALID
        pygame.draw.rect(surface, color, rect, 3)


def _render_multiline(font: pygame.font.Font, lines: List[str]) -> pygame.Surface:
    rendered_lines: List[pygame.Surface] = []
    width = 0
    height = 0
    for line in lines:
        surface = font.render(line, True, COLOR_TEXT)
        rendered_lines.append(surface)
        width = max(width, surface.get_width())
        height += surface.get_height() + 4
    result = pygame.Surface((width, height), pygame.SRCALPHA)
    y = 0
    for surface in rendered_lines:
        result.blit(surface, (0, y))
        y += surface.get_height() + 4
    return result


def draw_panel(surface: pygame.Surface, font: pygame.font.Font, city: City, selection: str) -> None:
    """Render the sidebar with resources and building selection."""

    panel_rect = pygame.Rect(GRID_WIDTH, 0, PANEL_WIDTH, surface.get_height())
    pygame.draw.rect(surface, COLOR_PANEL, panel_rect)

    lines = [
        "City of Nova Roma",
        f"Treasury: {city.treasury} denarii",
        f"Population: {city.population}",
        f"Food Stores: {city.food}",
        f"Happiness: {city.happiness}",
        "",
        "Buildings (press number keys):",
    ]
    for index, key in enumerate(BUILDING_ORDER, start=1):
        building = BUILDINGS[key]
        marker = "→" if key == selection else " "
        lines.append(f"{marker} {index}. {building.name} ({building.cost})")

    counts = city.count_buildings()
    lines.append("")
    lines.append("Totals:")
    for key in BUILDING_ORDER:
        lines.append(f"- {BUILDINGS[key].name}: {counts[key]}")

    instructions = _render_multiline(font, lines)
    surface.blit(instructions, (GRID_WIDTH + 12, 12))

    if city.history:
        recent_events = list(city.history)[-8:]
        history_lines = ["Recent events:"] + recent_events
        history_surface = _render_multiline(font, history_lines)
        surface.blit(
            history_surface,
            (GRID_WIDTH + 12, surface.get_height() - history_surface.get_height() - 12),
        )


def draw_background(surface: pygame.Surface) -> None:
    surface.fill(COLOR_BACKGROUND)

