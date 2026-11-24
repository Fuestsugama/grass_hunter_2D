import pygame
from pytmx.util_pygame import load_pygame
from settings import TILESIZE, MAP_TILESIZE, PLAYER_START_POS
from tile import Tile
from player import Player
from random import randint
from weapon import Weapon 
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer 
from upgrade import Upgrade
from game_over import GameOver
from sound import load_sound

class Level:
    """The game world: builds the map from Tiled, runs every sprite, and handles combat, XP, pause and game over."""
    def __init__(self):

        # get the display surface 
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        self.game_over = False 

        # sprite group setup
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites 
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # userinterface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        self.game_over_screen = GameOver()

        # sounds
        self.game_over_sound = load_sound('../assets/audio/game_over_jingle.ogg', 0.5)
        self.game_over_music = load_sound('../assets/audio/game_over.ogg', 0.4)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map (self):
        """Build the world from the Tiled map: floor image, walls, grass, objects, enemies, then the player."""
        tmx_data = load_pygame('../maps/world_map.tmx')
        floor_surf = pygame.Surface((tmx_data.width * TILESIZE, tmx_data.height * TILESIZE))

        layouts = {
            'floor': ['floor', 'detail'],             # flat ground: drawn once into the floor image
            'boundary': ['floor block'],              # invisible walls (coast, cliffs)
            'grass': ['grass'],
            'object': ['object', 'object layer 2'],
            'entities': ['entities'],                
        }

        for style, layer_names in layouts.items():
            for layer_name in layer_names:
                for col_index, row_index, gid in tmx_data.get_layer_by_name(layer_name):
                    if not gid:
                        continue    # empty cell in this layer
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
                    surf = pygame.transform.scale_by(tmx_data.get_tile_image_by_gid(gid), TILESIZE // MAP_TILESIZE)
                    properties = tmx_data.get_tile_properties_by_gid(gid) or {}

                    if style == 'floor':
                        floor_surf.blit(surf, (x,y))
                    elif style == 'boundary':
                        Tile((x,y), [self.obstacle_sprites], 'invisible')
                    elif style == 'grass':
                        Tile((x,y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'grass', surf)
                    elif style == 'object':   # solid unless "walkable = true" in Tiled
                        if properties.get('walkable'):
                            Tile((x,y), [self.visible_sprites], 'object', surf)
                        else:
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                    elif style == 'entities':
                        Enemy(
                            properties['monster'],
                            (x,y),
                            [self.visible_sprites, self.attackable_sprites],
                            self.obstacle_sprites,
                            self.damage_player,
                            self.trigger_death_particles,
                            self.add_exp)


        self.visible_sprites.floor_surf = floor_surf
        self.visible_sprites.floor_rect = floor_surf.get_rect(topleft = (0,0))

        self.player = Player(
            PLAYER_START_POS,
            [self.visible_sprites], 
            self.obstacle_sprites, 
            self.create_attack, 
            self.destroy_attack,
            self.create_magic)

    def create_attack (self):
        """Show the player's current weapon in their hand."""
        self.current_attack = Weapon(self.player,[self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        """Cast the selected spell ('heal' or 'flame') for the player."""
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, strength, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        """Remove the weapon from the player's hand when the attack ends."""
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        """Check what the player's weapon and spells touch: cut grass (with leaves) or damage enemies."""
        for attack_sprite in self.attack_sprites:
            collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
            for target_sprite in collision_sprites:
                if target_sprite.sprite_type == 'grass':
                    pos = target_sprite.rect.center
                    offset = pygame.math.Vector2(0,75)
                    for _ in range(randint(3, 6)):
                        self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
                    target_sprite.kill()
                else:
                    target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        """Hurt the player at most once per invulnerability window. At 0 health, switch to game over."""
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            
            # spawn particles 
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

            if self.player.health <= 0:
                self.player.health = 0  # to be sure that health never goes to negative values
                self.trigger_game_over()

    def trigger_game_over(self):
        """Freeze the game on the game over screen and switch to its music."""
        self.game_over = True
        pygame.mixer.stop()                     # stops the main music (and every other sound)
        self.game_over_sound.play()             # the jingle
        self.game_over_music.play(loops = -1)   # sad music that loops on the game over screen


            
    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos,[self.visible_sprites])

    def add_exp(self,amount):
        self.player.exp += amount

    def toggle_menu(self):

        self.game_paused = not self.game_paused

    def run(self):
        """Draw the frame, then update the game unless it is paused or over."""
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_over:
            self.game_over_screen.display()
        elif self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
    
       
class YsortCameraGroup(pygame.sprite.Group):
    """Sprite group with a camera that follows the player and draws lower sprites in front (depth)."""

    def __init__(self):
        # general setup 
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # the floor (floor_surf / floor_rect) is built from the Tiled map in Level.create_map

    def custom_draw(self, player):
        """Draw the floor, then every sprite sorted by its y position, offset so the player stays centred."""

        # getting the offset 
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor 
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos= sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        """Run the per-frame logic of every enemy that needs the player."""
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)