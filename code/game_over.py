import pygame 
from settings import *

class GameOver:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.big_font = pygame.font.Font(UI_FONT, 60)
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

    def display(self):
        # dark transparent layer over the frozen game
        overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.display_surface.blit(overlay, (0, 0))

        center = pygame.math.Vector2(self.display_surface.get_size()) / 2

        title = self.big_font.render('GAME OVER', False, HEALTH_COLOR)
        self.display_surface.blit(title, title.get_rect(center = center - (0, 40)))

        hint = self.font.render('Press R to restart the game', False, TEXT_COLOR)
        self.display_surface.blit(hint, hint.get_rect(center = center + (0, 40)))