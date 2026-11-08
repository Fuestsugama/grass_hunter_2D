# game setup
WIDTH    = 1280 
HEIGTH   = 720
FPS      = 60
TILESIZE = 64
MAP_TILESIZE = 16 # tile size used in Tiled (world_map.tmx)
HITBOX_OFFSET = {
    'player' : -26,
    'object' : -40, 
    'grass' : -10,
    'invisible' : 0
}


# UI  
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../assets/graphics/font/NormalFont.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111' 
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu 
TEXT_COLOR_SELECTED = '#111111'
BAR_C0LOR = '#EEEEEE'
BAR_C0LOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'



# Weapons 
weapon_data = {
    'sword' : {'cooldown': 100, 'damage': 15, 'graphic' : '../assets/graphics/weapons/sword/full.png'},
    'lance' : {'cooldown': 400, 'damage': 30, 'graphic' : '../assets/graphics/weapons/lance/full.png'},
    'axe' : {'cooldown': 300, 'damage': 20, 'graphic' : '../assets/graphics/weapons/axe/full.png'},
    'rapier' : {'cooldown': 50, 'damage': 10, 'graphic' : '../assets/graphics/weapons/rapier/full.png'},
    'sai' : {'cooldown': 80, 'damage': 8, 'graphic' : '../assets/graphics/weapons/sai/full.png'}
}

# magic
magic_data = {
    'flame' : {'strength': 5, 'cost': 20, 'graphic' : '../assets/graphics/particles/flame/fire.png'},
    'heal' : {'strength': 20, 'cost': 10, 'graphic' : '../assets/graphics/particles/heal/heal.png'}
}


# enemy
monster_data = {
    'slime3' : {'health': 80, 'exp': 50, 'damage': 10, 'attack_type': 'slash','speed': 2, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 300, 'attack_sound':'../assets/audio/enemy_attack.wav'},
    'flam' : {'health': 90, 'exp': 100, 'damage': 30, 'attack_type': 'fireball','speed': 3, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400, 'attack_sound':'../assets/audio/fireball.wav'},
    'gold_racoon' : {'health': 70, 'exp': 80, 'damage': 20, 'attack_type': 'claw','speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300, 'attack_sound':'../assets/audio/monster_attack.wav'},
    'trex' : {'health': 120, 'exp': 150, 'damage': 40, 'attack_type': 'bite','speed': 2, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 350, 'attack_sound':'../assets/audio/monster_attack.wav'},
    'spider_yellow' : {'health': 60, 'exp': 70, 'damage': 15, 'attack_type': 'bite','speed': 4, 'resistance': 3, 'attack_radius': 40, 'notice_radius': 250, 'attack_sound':'../assets/audio/monster_attack.wav'},
    'mole' : {'health': 100, 'exp': 120, 'damage': 25, 'attack_type': 'dig','speed': 2, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 300, 'attack_sound':'../assets/audio/monster_attack.wav'},
    'snake3' : {'health': 70, 'exp': 60, 'damage': 15, 'attack_type': 'bite','speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300, 'attack_sound':'../assets/audio/monster_attack.wav'},
    'tengu_blue' : {'health': 300, 'exp': 300, 'damage': 50, 'attack_type': 'slash','speed': 3, 'resistance': 3, 'attack_radius': 100, 'notice_radius': 400, 'attack_sound':'../assets/audio/monster_attack.wav'},
}   