import pygame
import os

WIDTH = 1920  # 游戏窗口的宽度
HEIGHT = 1200  # 游戏窗口的高度
FPS = 1000  # 帧率

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 215, 0)
GREY = (28, 28, 28)

# player & enemy image resource

game_folder = os.path.dirname(__file__)

img_folder = os.path.join(game_folder, 'img')

player_img = pygame.image.load(os.path.join(img_folder, 'player1.png'))
player_img = pygame.transform.rotozoom(player_img, 0, 0.1)

enemy_img = pygame.image.load(os.path.join(img_folder, 'enemy.png'))
enemy_img = pygame.transform.rotozoom(enemy_img, 135, 0.1)

bullet_img = pygame.image.load(os.path.join(img_folder, 'bullet2.png'))
bullet_img = pygame.transform.rotozoom(bullet_img, 0, 0.08)

enemy_bullet_img = pygame.image.load(os.path.join(img_folder, 'bullet1.png'))
enemy_bullet_img = pygame.transform.rotozoom(enemy_bullet_img, 0, 0.2)

boss_img = pygame.image.load(os.path.join(img_folder, 'boss.png'))
boss_img = pygame.transform.rotozoom(boss_img, 0, 1)


# prop image resource
amo_img = pygame.image.load(os.path.join(img_folder, 'amo.png'))
amo_img = pygame.transform.rotozoom(amo_img, 0, 0.1)

hp_img = pygame.image.load(os.path.join(img_folder, 'hp.png'))
hp_img = pygame.transform.rotozoom(hp_img, 0, 0.15)

fuel_img = pygame.image.load(os.path.join(img_folder, 'fuel.png'))
fuel_img = pygame.transform.rotozoom(fuel_img, 0, 0.15)

Event_img = dict()
Event_img[1] = hp_img
Event_img[2] = amo_img
Event_img[3] = fuel_img

# video resource

video_folder = os.path.join(game_folder, 'video')
first_video = os.path.join(video_folder, 'Apex Legends.mp4')

# resource
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
bg_img = pygame.image.load(os.path.join(img_folder, 'bg.jpg'))
bg_img = pygame.transform.scale(bg_img, (1920, 1200))

hpBar_img = pygame.image.load(os.path.join(img_folder, 'bar1.png'))
hpBar_img = pygame.transform.rotozoom(hpBar_img, 0, 0.8)

music_folder = os.path.join(game_folder, 'music')

# game setting
winPoint = 25
NormalEnemyCreatePossibility = 3
NormalPropCreatePossibility = 1
prop_hp = 2
prop_load = 20
prop_fuel = 500