import pygame
from pytmx.util_pygame import load_pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from weapon import Weapon 
from ui import UI

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
        scale = TILESIZE // MAP_TILESIZE

        # flat layers (floor + detail): drawn once into the floor image, under everything
        floor_surf = pygame.Surface((tmx_data.width * TILESIZE, tmx_data.height * TILESIZE))
        for layer_name in ('floor', 'detail'):
            for x, y, surf in tmx_data.get_layer_by_name(layer_name).tiles():
                floor_surf.blit(pygame.transform.scale_by(surf, scale), (x * TILESIZE, y * TILESIZE))
        self.visible_sprites.floor_surf = floor_surf
        self.visible_sprites.floor_rect = floor_surf.get_rect(topleft = (0,0))

        # invisible walls (coast, cliffs)
        for x, y, surf in tmx_data.get_layer_by_name('floor block').tiles():
            Tile((x * TILESIZE, y * TILESIZE), [self.obstacle_sprites], 'invisible')

        # grass and objects: Y-sorted, and solid unless the tile has "walkable = true" in Tiled
        for layer_name, sprite_type in (('grass', 'grass'), ('object', 'object'), ('object layer 2', 'object')):
            for x, y, gid in tmx_data.get_layer_by_name(layer_name):
                if gid:
                    surf = pygame.transform.scale_by(tmx_data.get_tile_image_by_gid(gid), scale)
                    properties = tmx_data.get_tile_properties_by_gid(gid) or {}
                    groups = [self.visible_sprites] if properties.get('walkable') else [self.visible_sprites, self.obstacle_sprites]
                    Tile((x * TILESIZE, y * TILESIZE), groups, sprite_type, surf)

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