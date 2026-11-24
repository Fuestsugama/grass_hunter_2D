"""Checks on the game data: the Tiled map and settings.py must agree."""
from pytmx.util_pygame import load_pygame

from settings import monster_data
from support import frame_number, import_folder


def monsters_placed_in_tiled():
    tmx_data = load_pygame('../maps/world_map.tmx')
    names = set()
    for _, _, gid in tmx_data.get_layer_by_name('entities'):
        if gid:
            names.add(tmx_data.get_tile_properties_by_gid(gid)['monster'])
    return names


def test_every_monster_in_the_map_is_defined_in_settings():
    assert monsters_placed_in_tiled() <= set(monster_data)


def test_every_monster_has_its_animation_frames():
    for monster_name in monster_data:
        for animation in ('idle', 'move', 'attack'):
            assert import_folder(f'../assets/graphics/monsters/{monster_name}/{animation}'), \
                f'{monster_name} has no {animation} frames'


def test_frames_are_sorted_by_number_not_alphabetically():
    files = ['10.png', '2.png', '0.png', '1.png']
    assert sorted(files, key=frame_number) == ['0.png', '1.png', '2.png', '10.png']
