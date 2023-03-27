import pygame, random
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
from os import listdir

pygame.init()
FPS = pygame.time.Clock()
sreen = width, height = 1920, 1080
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 0, 255)

font = pygame.font.SysFont('Verdana', 40)
main_surface = pygame.display.set_mode(sreen)
images_path = 'goose'
player_images = [pygame.image.load(images_path + '/' + file).convert_alpha() for file in listdir(images_path)]
scores = 0
img_index = 0
enemies = []
bonuses = []

ball = player_images[0]
ball_rect = ball.get_rect()
ball_speed = 10

def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy.png'), (50, 50))
    enemy_rect = pygame.Rect(width, random.randint(1, height), *enemy.get_size())
    enemy_speed = random.randint(3, 5)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (50, 80))
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonus_speed = random.randint(4, 6)
    return [bonus, bonus_rect, bonus_speed]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 100)

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), sreen)
bgX, bgX2, bg_spped = 0, bg.get_width(), 2

is_working = True
while is_working:
    FPS.tick(60)
    for i in pygame.event.get():
        if i.type == QUIT:
            is_working = False
        if i.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if i.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if i.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_images):
                img_index = 0
            ball = player_images[img_index]

    pressed_key = pygame.key.get_pressed()
    bgX -= bg_spped
    bgX2 -= bg_spped
    if bgX < -bg.get_width():
        bgX = bg.get_width()
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))
    main_surface.blit(ball, ball_rect)
    main_surface.blit(font.render(str(scores), True, BLACK), (width-30, 10))
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        elif ball_rect.colliderect(enemy[1]):
            is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])
        if bonus[1].bottom >= height:
            bonuses.pop(bonuses.index(bonus))
        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressed_key[K_DOWN] and not ball_rect.bottom >= height:
        ball_rect = ball_rect.move(0, ball_speed)
    elif pressed_key[K_UP] and not ball_rect.top <= 0:
        ball_rect = ball_rect.move(0, -ball_speed)
    elif pressed_key[K_RIGHT] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(ball_speed, 0)
    elif pressed_key[K_LEFT] and not ball_rect.left <= 0:
        ball_rect = ball_rect.move(-ball_speed, 0)

    pygame.display.flip()