import pygame
from pytmx.util_pygame import load_pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from weapon import Weapon 
from ui import UI
from enemy import Enemy

class Level:
    def __init__(self):

        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites 
        self.current_attack = None

        # sprite setup
        self.create_map()

        # userinterface
        self.ui = UI()

    def create_map (self):
        tmx_data = load_pygame('../maps/world_map.tmx')
        floor_surf = pygame.Surface((tmx_data.width * TILESIZE, tmx_data.height * TILESIZE))

        for layer in tmx_data.layers:
            for x, y, gid in layer:
                if not gid:
                    continue
                pos = (x * TILESIZE, y * TILESIZE)
                surf = pygame.transform.scale_by(tmx_data.get_tile_image_by_gid(gid), TILESIZE // MAP_TILESIZE)
                properties = tmx_data.get_tile_properties_by_gid(gid) or {}

                if layer.name in ('floor', 'detail'):   # flat ground: drawn once into the floor image
                    floor_surf.blit(surf, pos)
                elif layer.name == 'floor block':       # invisible walls (coast, cliffs)
                    Tile(pos, [self.obstacle_sprites], 'invisible')
                elif layer.name == 'entities':          # monsters placed in Tiled, "monster" property = folder name
                    Enemy(properties['monster'], pos, [self.visible_sprites], self.obstacle_sprites)
                else:                                   # grass and objects: solid unless "walkable = true" in Tiled
                    groups = [self.visible_sprites] if properties.get('walkable') else [self.visible_sprites, self.obstacle_sprites]
                    Tile(pos, groups, 'grass' if layer.name == 'grass' else 'object', surf)

        self.visible_sprites.floor_surf = floor_surf
        self.visible_sprites.floor_rect = floor_surf.get_rect(topleft = (0,0))

        self.player = Player(
            (2050,1500), 
            [self.visible_sprites], 
            self.obstacle_sprites, 
            self.create_attack, 
            self.destroy_attack,
            self.create_magic)

    def create_attack (self):
        self.current_attack = Weapon(self.player,[self.visible_sprites])

    def create_magic(self, style, strength, cost):
        print(style, strength, cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):

        #update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)
       
class YsortCameraGroup(pygame.sprite.Group):

    def __init__(self):
        # general setup 
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # the floor (floor_surf / floor_rect) is built from the Tiled map in Level.create_map

    def custom_draw(self, player):

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
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)