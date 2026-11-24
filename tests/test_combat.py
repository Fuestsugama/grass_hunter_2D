"""Rules of combat: damage, invulnerability after a hit, death, XP and game over."""
import pygame

from settings import monster_data


def an_enemy(level):
    return next(sprite for sprite in level.attackable_sprites if sprite.sprite_type == 'enemy')


# --- player hurt by a monster ---

def test_player_loses_health_when_hit(level, player):
    level.damage_player(10, 'claw')
    assert player.health == 90


def test_player_is_invulnerable_just_after_a_hit(level, player):
    level.damage_player(10, 'claw')
    level.damage_player(10, 'claw')          # second hit, same moment
    assert player.health == 90


def test_health_never_goes_below_zero(level, player):
    level.damage_player(1000, 'claw')
    assert player.health == 0


def test_game_over_when_health_reaches_zero(level, player):
    level.damage_player(player.health, 'claw')
    assert level.game_over


# --- enemy hurt by the player ---

def test_weapon_hit_removes_the_player_weapon_damage(level, player):
    enemy = an_enemy(level)
    health_before = enemy.health
    enemy.get_damage(player, 'weapon')
    assert enemy.health == health_before - player.get_full_weapon_damage()


def test_enemy_is_invulnerable_just_after_a_hit(level, player):
    enemy = an_enemy(level)
    enemy.get_damage(player, 'weapon')
    health_after_first_hit = enemy.health
    enemy.get_damage(player, 'weapon')
    assert enemy.health == health_after_first_hit


def test_dead_enemy_disappears_and_gives_its_exp(level, player):
    enemy = an_enemy(level)
    exp_before = player.exp
    enemy.health = 0
    enemy.check_death()
    assert not enemy.alive()
    assert player.exp == exp_before + monster_data[enemy.monster_name]['exp']


def test_enemy_on_top_of_the_player_does_not_crash(level, player):
    enemy = an_enemy(level)
    enemy.rect.center = player.rect.center
    distance, direction = enemy.get_player_distance_direction(player)
    assert distance == 0
    assert direction == pygame.math.Vector2(0, 0)


def test_enemy_attacks_when_close_and_ignores_the_player_when_far(level, player):
    enemy = an_enemy(level)
    enemy.rect.center = player.rect.center
    enemy.get_status(player)
    assert enemy.status == 'attack'
    enemy.rect.center = (player.rect.centerx + enemy.notice_radius + 100, player.rect.centery)
    enemy.get_status(player)
    assert enemy.status == 'idle'
