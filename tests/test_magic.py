"""Rules of the spells: energy cost, healing limit, refusal without energy."""
from settings import magic_data

HEAL = magic_data['heal']
FLAME = magic_data['flame']


def cast(level, spell):
    level.create_magic(spell, magic_data[spell]['strength'], magic_data[spell]['cost'])


def test_heal_restores_health_and_costs_energy(level, player):
    player.health = 50
    energy_before = player.energy
    cast(level, 'heal')
    assert player.health == 50 + HEAL['strength']
    assert player.energy == energy_before - HEAL['cost']


def test_heal_never_goes_above_max_health(level, player):
    player.health = player.stats['health'] - 1
    cast(level, 'heal')
    assert player.health == player.stats['health']


def test_spells_refused_without_enough_energy(level, player):
    player.health = 50
    player.energy = 0
    cast(level, 'heal')
    cast(level, 'flame')
    assert player.health == 50
    assert player.energy == 0
    assert len(level.attack_sprites) == 0    # no flame was created


def test_flame_costs_energy_and_creates_fire(level, player):
    energy_before = player.energy
    cast(level, 'flame')
    assert player.energy == energy_before - FLAME['cost']
    assert len(level.attack_sprites) == 5    # five bursts of fire
