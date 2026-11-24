import pygame 
from settings import TILESIZE
from random import randint
from sound import load_sound

class MagicPlayer:
    """Applies the spells: their energy cost, their effect and their particles."""
    def __init__ (self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal': load_sound('../assets/audio/heal.ogg'),
            'flame' : load_sound('../assets/audio/Fire.ogg')
        }

    def heal(self, player, strength, cost, groups):
        """Restore health without passing the max, if the player has enough energy."""

        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost 
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center, groups)

    def flame(self, player, strength, cost, groups):
        """Send five bursts of fire in the direction the player faces, if the player has enough energy."""
        if player.energy >= cost:
            player.energy -= cost 
            self.sounds['flame'].play()

            if player.status.split('_')[0] =='right': direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0] =='left': direction = pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0] =='up': direction = pygame.math.Vector2(0,-1)
            else: direction = pygame.math.Vector2(0,1)

            for i in range(1,6): # offset of 1 ==> cast the spell at at least a range of 1 so 64 pixels 
                if direction.x: #horizontal
                    offset_x = (direction.x * i ) * TILESIZE
                    x = player.rect.centerx + offset_x + randint( -TILESIZE // 3, TILESIZE // 3) # render effect 
                    y = player.rect.centery + randint( -TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x,y), groups)

                else:  # vertical 
                    offset_y = (direction.y * i ) * TILESIZE
                    x = player.rect.centerx  + randint( -TILESIZE // 3, TILESIZE // 3) # render effect 
                    y = player.rect.centery  + offset_y + randint( -TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x,y), groups)