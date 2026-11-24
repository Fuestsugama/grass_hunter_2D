"""Shared test setup: run pygame without a window or sound card, from the code folder."""
import os
import sys

import pytest

CODE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'code')
os.environ['SDL_VIDEODRIVER'] = 'dummy'   # no window
os.environ['SDL_AUDIODRIVER'] = 'dummy'   # no sound card needed
os.chdir(CODE_DIR)                        # the game loads its assets with paths like '../assets'
sys.path.insert(0, CODE_DIR)

import pygame
pygame.init()
pygame.display.set_mode((1280, 720))

from level import Level


@pytest.fixture
def level():
    """A fresh game world (map, player, enemies) for each test."""
    return Level()


@pytest.fixture
def player(level):
    return level.player
