"""Constants used across the OpenCaesar project."""

import pygame

# Rendering
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 30

# Grid
GRID_COLS = 24
GRID_ROWS = 18
TILE_SIZE = 32
GRID_WIDTH = GRID_COLS * TILE_SIZE
GRID_HEIGHT = GRID_ROWS * TILE_SIZE

# Colors
COLOR_BACKGROUND = pygame.Color(28, 31, 38)
COLOR_GRID = pygame.Color(60, 63, 72)
COLOR_PANEL = pygame.Color(18, 19, 24)
COLOR_TEXT = pygame.Color(245, 245, 245)
COLOR_INVALID = pygame.Color(171, 52, 42)
COLOR_VALID = pygame.Color(90, 141, 56)

PANEL_WIDTH = WINDOW_WIDTH - GRID_WIDTH
FONT_NAME = "freesansbold.ttf"

SIMULATION_TICK_MS = 1500

