import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import pytest
from pygame.locals import K_SPACE, K_a, K_d, K_w, K_s

import main


# Setup

class FakeKeys:
    def __init__(self, *pressed):
        self.pressed = pressed

    def __getitem__(self, key):
        return key in self.pressed


def press(monkeypatch, *keys):
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: FakeKeys(*keys))


class FakeClock:
    def __init__(self):
        self.now = 10000


@pytest.fixture
def clock(monkeypatch):
    fake = FakeClock()
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: fake.now)
    return fake


@pytest.fixture(autouse=True)
def fresh_game(clock, monkeypatch):
    monkeypatch.setattr(main, "joystick", None)
    press(monkeypatch)
    main.bullet_group.empty()
    main.alien_group.empty()
    main.alien_bullet_group.empty()
    main.spaceship.lives = 3
    main.spaceship.rect.center = main.spaceship.start_pos
    main.spaceship.invincible_until = 0
    main.spaceship.last_shot = 0
    main.spaceship_group.add(main.spaceship)


def alien_bullet_on_player():
    bullet = main.AlienBullet(*main.spaceship.rect.center)
    main.alien_bullet_group.add(bullet)
    bullet.update()


#Normal Tests

def test_space_fires_a_bullet(monkeypatch):
    press(monkeypatch, K_SPACE)
    main.spaceship.update()
    assert len(main.bullet_group) == 1


def test_holding_space_fires_several_bullets(monkeypatch, clock):
    press(monkeypatch, K_SPACE)
    for _ in range(3):
        main.spaceship.update()
        clock.now += 401
    assert len(main.bullet_group) == 3


def test_bullet_kills_alien_it_hits():
    main.alien_group.add(main.Alien(300, 300))
    bullet = main.Bullet(300, 300)
    main.bullet_group.add(bullet)
    bullet.update()
    assert len(main.alien_group) == 0


def test_alien_bullet_hit_costs_one_life():
    alien_bullet_on_player()
    assert main.spaceship.lives == 2


def test_player_respawns_at_start_position():
    main.spaceship.rect.center = (100, 500)
    alien_bullet_on_player()
    assert main.spaceship.rect.center == main.spaceship.start_pos


#Boundary Tests

def test_cannot_shoot_again_before_cooldown(monkeypatch, clock):
    press(monkeypatch, K_SPACE)
    main.spaceship.update()
    clock.now += 100
    main.spaceship.update()
    assert len(main.bullet_group) == 1


def test_invincibility_lasts_exactly_2_seconds(clock):
    alien_bullet_on_player()
    clock.now += 1999
    assert main.spaceship.is_invincible() == True
    clock.now += 1
    assert main.spaceship.is_invincible() == False


@pytest.mark.parametrize("key, edge, value", [
    (K_a, "left", 0),
    (K_d, "right", main.screen_width),
    (K_w, "top", 0),
    (K_s, "bottom", main.screen_height),
    ])
def test_player_cannot_leave_screen(monkeypatch, key, edge, value):
    setattr(main.spaceship.rect, edge, value)
    press(monkeypatch, key)
    main.spaceship.update()
    assert getattr(main.spaceship.rect, edge) == value


def test_losing_last_life_is_game_over():
    main.spaceship.lives = 1
    alien_bullet_on_player()
    assert main.spaceship.update() == -1


#Failure Tests

def test_alien_bullet_that_misses_costs_no_life():
    bullet = main.AlienBullet(0, 0)
    main.alien_bullet_group.add(bullet)
    bullet.update()
    assert main.spaceship.lives == 3


def test_hit_while_invincible_costs_no_life():
    alien_bullet_on_player()
    alien_bullet_on_player()
    assert main.spaceship.lives == 2


def test_player_bullet_that_misses_kills_nothing():
    main.alien_group.add(main.Alien(300, 300))
    bullet = main.Bullet(50, 700)
    main.bullet_group.add(bullet)
    bullet.update()
    assert len(main.alien_group) == 1
