# game setup
WIDTH    = 1280 
HEIGTH   = 720
FPS      = 60
TILESIZE = 64
MAP_TILESIZE = 16 # tile size used in Tiled (world_map.tmx)
 
# Weapons 

weapon_data = {
    'sword' : {'cooldown': 100, 'damage': 15, 'graphic' : '../assets/graphics/weapons/sword/full.png'},
    'lance' : {'cooldown': 400, 'damage': 30, 'graphic' : '../assets/graphics/weapons/lance/full.png'},
    'axe' : {'cooldown': 300, 'damage': 20, 'graphic' : '../assets/graphics/weapons/axe/full.png'},
    'rapier' : {'cooldown': 50, 'damage': 10, 'graphic' : '../assets/graphics/weapons/rapier/full.png'},
    'sai' : {'cooldown': 80, 'damage': 8, 'graphic' : '../assets/graphics/weapons/sai/full.png'}
}