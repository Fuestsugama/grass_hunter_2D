"""Rules of the player's stats: damage formulas and energy refill."""
from settings import weapon_data, magic_data


def test_weapon_damage_is_attack_stat_plus_weapon_damage(player):
    player.weapon = 'sword'
    assert player.get_full_weapon_damage() == player.stats['attack'] + weapon_data['sword']['damage']


def test_spell_damage_is_magic_stat_plus_spell_strength(player):
    player.magic = 'flame'
    assert player.get_full_magic_damage() == player.stats['magic'] + magic_data['flame']['strength']


def test_energy_refills_over_time(player):
    player.energy = 0
    player.energy_recovery()
    assert player.energy > 0


def test_energy_never_goes_above_the_max(player):
    player.energy = player.stats['energy'] + 5
    player.energy_recovery()
    assert player.energy == player.stats['energy']
