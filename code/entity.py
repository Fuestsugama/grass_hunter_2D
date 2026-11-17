import pygame
import settings
from math import sin

class Entity(pygame.sprite.Sprite):
    """Base class for everything that moves and collides: the player and the enemies."""
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = settings.ANIMATION_SPEED
        self.direction = pygame.math.Vector2()

    def move(self,speed):
            """Move along the current direction, checking collisions one axis at a time."""
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.hitbox.x  += self.direction.x * speed
            self.collision('horizontal')
            self.hitbox.y  += self.direction.y * speed
            self.collision('vertical')
            self.rect.center = self.hitbox.center

    def collision(self, direction):
        """Push the hitbox out of any obstacle it overlaps on one axis ('horizontal' or 'vertical')."""

        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0 : # moving right 
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0 : # moving left 
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0 : # moving down 
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0 : # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        """Return 255 or 0 alternately over time, used to make a hit sprite flicker."""
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def flicker(self):
        """Blink while invulnerable after a hit, fully visible otherwise."""
        if not self.vulnerable:
            self.image.set_alpha(self.wave_value())
        else:
            self.image.set_alpha(255)
