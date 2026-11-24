"""Rules of the upgrade menu: spend XP to raise a stat, never above its maximum."""
from settings import PLAYER_STATS, PLAYER_MAX_STATS, PLAYER_UPGRADE_COST, UPGRADE_STAT_FACTOR, UPGRADE_COST_FACTOR
from upgrade import Item

HEALTH = 0   # position of 'health' in the menu


def upgrade_health(player):
    Item(0, 0, 100, 100, HEALTH, font=None).trigger(player)


def test_upgrade_spends_exp_and_raises_the_stat(player):
    player.exp = 1000
    upgrade_health(player)
    assert player.exp == 1000 - PLAYER_UPGRADE_COST['health']
    assert player.stats['health'] == PLAYER_STATS['health'] * UPGRADE_STAT_FACTOR


def test_upgrade_makes_the_next_one_more_expensive(player):
    upgrade_health(player)
    assert player.upgrade_cost['health'] == PLAYER_UPGRADE_COST['health'] * UPGRADE_COST_FACTOR


def test_upgrade_never_goes_above_the_max(player):
    player.stats['health'] = 290        # 290 * 1.2 = 348, must stop at 300
    upgrade_health(player)
    assert player.stats['health'] == PLAYER_MAX_STATS['health']


def test_upgrade_refused_without_enough_exp(player):
    player.exp = PLAYER_UPGRADE_COST['health'] - 1
    upgrade_health(player)
    assert player.stats['health'] == PLAYER_STATS['health']
    assert player.exp == PLAYER_UPGRADE_COST['health'] - 1


def test_upgrade_refused_when_the_stat_is_at_max(player):
    player.stats['health'] = PLAYER_MAX_STATS['health']
    exp_before = player.exp
    upgrade_health(player)
    assert player.exp == exp_before


def test_upgrades_do_not_change_the_settings(player):
    upgrade_health(player)
    assert PLAYER_STATS['health'] == 100
    assert PLAYER_UPGRADE_COST['health'] == 100
