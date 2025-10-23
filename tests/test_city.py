"""Basic tests for the city simulation."""

import os

import pygame

from open_caesar.city import City


def setup_module(module):
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.display.init()


def teardown_module(module):
    pygame.display.quit()


def test_place_and_demolish():
    city = City()
    assert city.place("house", (0, 0))
    assert city.grid[0][0] == "house"
    treasury_after_purchase = city.treasury
    assert treasury_after_purchase < 400
    assert city.demolish((0, 0))
    assert city.grid[0][0] is None
    assert city.treasury >= treasury_after_purchase


def test_iteration_effects():
    city = City()
    city.place("farm", (0, 0))
    city.place("market", (1, 0))
    city.iterate()
    assert city.food >= 0
    assert city.treasury >= 400 - 40 - 60  # spent funds + income
    assert 0 <= city.happiness <= 100

