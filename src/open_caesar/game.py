"""Executable entry point for OpenCaesar."""

from __future__ import annotations

import pygame

from .buildings import BUILDINGS, BUILDING_ORDER
from .city import City
from .constants import (
    FPS,
    GRID_WIDTH,
    SIMULATION_TICK_MS,
    TILE_SIZE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    FONT_NAME,
)
from .ui import draw_background, draw_grid, draw_panel


class Game:
    """Main application class containing the event loop."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("OpenCaesar")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.city = City()
        self.font = pygame.font.Font(FONT_NAME, 20)
        self.building_index = 0
        self.selected_building = BUILDING_ORDER[self.building_index]
        self.simulation_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.simulation_event, SIMULATION_TICK_MS)
        self.highlight_tile = None
        self.can_build = False

    def run(self) -> None:
        while True:
            self.clock.tick(FPS)
            if not self.handle_events():
                break
            self.render()
        pygame.quit()

    # Event handling -----------------------------------------------------
    def handle_events(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        highlight_tile = None
        can_build = False

        if mouse_pos[0] < GRID_WIDTH:
            highlight_tile = (mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE)
            can_build = self.city.can_place(self.selected_building, highlight_tile)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == self.simulation_event:
                self.city.iterate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                self.handle_keydown(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN and highlight_tile is not None:
                if event.button == 1 and can_build:
                    self.city.place(self.selected_building, highlight_tile)
                elif event.button == 3:
                    self.city.demolish(highlight_tile)

        self.highlight_tile = highlight_tile
        self.can_build = can_build
        return True

    def handle_keydown(self, key: int) -> None:
        if pygame.K_1 <= key <= pygame.K_9:
            index = key - pygame.K_1
            if index < len(BUILDING_ORDER):
                self.building_index = index
                self.selected_building = BUILDING_ORDER[self.building_index]
        elif key == pygame.K_TAB:
            self.building_index = (self.building_index + 1) % len(BUILDING_ORDER)
            self.selected_building = BUILDING_ORDER[self.building_index]
        elif key == pygame.K_SPACE:
            self.city.iterate()

    # Rendering ----------------------------------------------------------
    def render(self) -> None:
        draw_background(self.screen)
        draw_grid(
            self.screen,
            self.city,
            highlight_pos=self.highlight_tile,
            valid=self.can_build,
        )
        draw_panel(self.screen, self.font, self.city, self.selected_building)
        pygame.display.flip()


def main() -> None:
    Game().run()


if __name__ == "__main__":
    main()

