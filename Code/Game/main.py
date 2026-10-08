import pygame
from pygame.locals import *
import random

#by salman, naji, tyler
#wassup brochachos
pygame.init()

pygame.joystick.init()
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Controller connected:", joystick.get_name())
else:
    print("No controller found")

clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')

font40 = pygame.font.SysFont('Impact', 40)

shoot_sound = pygame.mixer.Sound("shoot.wav")
shoot_sound.set_volume(0.5)

rows = 3
cols = 5
alien_cooldown = 1000
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0

boss_active = False
boss_health_start = 10
boss_health = boss_health_start
boss_last_shot = pygame.time.get_ticks()
boss_cooldown = 700

red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)

player_img = pygame.image.load('player.png').convert_alpha()
enemy_img = pygame.image.load('enemy.png').convert_alpha()

player_img = pygame.transform.scale(player_img, (50, 30))
enemy_img = pygame.transform.scale(enemy_img, (40, 25))
enemy_img = pygame.transform.rotate(enemy_img, 180)
boss_img = pygame.transform.scale(enemy_img, (120, 40))

def draw_text(text, x, y):
    img = font40.render(text, True, white)
    screen.blit(img, (x, y))

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(x, y))
        self.health = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        speed = 8
        cooldown = 400
        result = 0

        key = pygame.key.get_pressed()
        if key[K_a] and self.rect.left > 0:
            self.rect.x -= speed
        if key[K_d] and self.rect.right < screen_width:
            self.rect.x += speed
        if key[K_w] and self.rect.top > 0:
            self.rect.y -= speed
        if key[K_s] and self.rect.bottom < screen_height:
            self.rect.y += speed

        time_now = pygame.time.get_ticks()
        if key[K_SPACE] and time_now - self.last_shot > cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            shoot_sound.play()
            self.last_shot = time_now

        global joystick
        if joystick is not None:
            axis_x = joystick.get_axis(0)  # left/right
            axis_y = joystick.get_axis(1)  # up/down
            deadzone = 0.2

            if axis_x < -deadzone and self.rect.left > 0:
                self.rect.x -= speed
            if axis_x > deadzone and self.rect.right < screen_width:
                self.rect.x += speed

            if axis_y < -deadzone and self.rect.top > 0:
                self.rect.y -= speed
            if axis_y > deadzone and self.rect.bottom < screen_height:
                self.rect.y += speed

            shoot_button = joystick.get_button(0)
            time_now2 = pygame.time.get_ticks()
            if shoot_button and time_now2 - self.last_shot > cooldown:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                bullet_group.add(bullet)
                shoot_sound.play()
                self.last_shot = time_now2

        pygame.draw.rect(screen, red, (self.rect.x, self.rect.bottom + 10, 50, 10))
        pygame.draw.rect(screen, green, (self.rect.x, self.rect.bottom + 10,
                                         50 * (self.health / 3), 10))

        if self.health <= 0:
            self.kill()
            result = -1

        return result

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill(yellow)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        global boss_health
        self.rect.y -= 6

        if self.rect.bottom < 0:
            self.kill()
            return

        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()

        if boss_active:
            if pygame.sprite.spritecollide(self, boss_group, False):
                self.kill()
                boss_health -= 1

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(center=(x, y))
        self.move_dir = 1
        self.counter = 0

    def update(self):
        self.rect.x += self.move_dir
        self.counter += 1
        if abs(self.counter) > 60:
            self.move_dir *= -1
            self.counter *= -1

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=3):
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill(white)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > screen_height:
            self.kill()
            return

        if pygame.sprite.spritecollide(self, spaceship_group, False):
            self.kill()
            spaceship.health -= 1

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = boss_img
        self.rect = self.image.get_rect(center=(x, y))
        self.move_dir = 3

    def update(self):
        self.rect.x += self.move_dir
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.move_dir *= -1

spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

def create_aliens():
    for row in range(rows):
        for col in range(cols):
            alien = Alien(120 + col * 90, 80 + row * 60)
            alien_group.add(alien)

create_aliens()

spaceship = Spaceship(screen_width // 2, screen_height - 100, 3)
spaceship_group.add(spaceship)

run = True
while run:
    clock.tick(fps)
    screen.fill(black)

    if countdown == 0:
        time_now = pygame.time.get_ticks()

        if not boss_active:
            if time_now - last_alien_shot > alien_cooldown and len(alien_group) > 0:
                alien = random.choice(alien_group.sprites())
                bullet = AlienBullet(alien.rect.centerx, alien.rect.bottom)
                alien_bullet_group.add(bullet)
                last_alien_shot = time_now

            if len(alien_group) == 0 and game_over == 0:
                boss = Boss(screen_width // 2, 120)
                boss_group.add(boss)
                boss_active = True
                boss_health = boss_health_start

        if boss_active and len(boss_group) > 0 and game_over == 0:
            if time_now - boss_last_shot > boss_cooldown:
                boss_sprite = boss_group.sprites()[0]
                bullet = AlienBullet(boss_sprite.rect.centerx, boss_sprite.rect.bottom, speed=5)
                alien_bullet_group.add(bullet)
                boss_last_shot = time_now

        if game_over == 0:
            game_over = spaceship.update()
            bullet_group.update()
            alien_group.update()
            alien_bullet_group.update()
            boss_group.update()

            if boss_active and boss_health <= 0:
                boss_group.empty()
                game_over = 1

        else:
            if game_over == -1:
                draw_text('GAME OVER!', screen_width // 2 - 120, screen_height // 2)
            if game_over == 1:
                draw_text('YOU WIN!', screen_width // 2 - 120, screen_height // 2)

    else:
        draw_text("GET READY!", screen_width // 2 - 120, screen_height // 2)
        draw_text(str(countdown), screen_width // 2 - 10, screen_height // 2 + 60)

        if pygame.time.get_ticks() - last_count > 1000:
            countdown -= 1
            last_count = pygame.time.get_ticks()

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    boss_group.draw(screen)

    if boss_active and len(boss_group) > 0:
        draw_text(f"Boss HP: {boss_health}", 10, 10)

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    pygame.display.update()

pygame.quit()
