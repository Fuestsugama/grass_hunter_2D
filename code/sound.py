"""Loads the game's sounds once and shares them between all classes."""
import pygame

_loaded_sounds = {}

def load_sound(path, volume=1.0):
    """Load a sound the first time it is asked for, then reuse it; set its volume."""
    if path not in _loaded_sounds:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        _loaded_sounds[path] = sound
    return _loaded_sounds[path]
