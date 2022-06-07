import pygame
import os
import random

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

# object class


class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, img=player_img, hp=10, speed=2, load=1000, fuel=5000):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)

        # create a plain rectangle for the sprite image
        self.image = img
        self.image.set_colorkey(BLACK)

        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()

        # center the sprite on the screen
        self.rect.center = (self.rect.width / 2, HEIGHT / 2)

        # player's speed
        self.speed = speed
        self.speed_limit = speed * 2

        # amo
        self.gun_pos = None

        self.bullets = pygame.sprite.Group()
        self.load = load
        self.load_full = load

        # hit point
        self.hp = hp
        self.hp_full = hp
        self.shield = 10

        self.lifebar = Lifebar(self)

        # fuel
        self.fuel = fuel
        self.fuel_full = fuel
        self.speed_up = False

    def reset(self):
        self.__init__()

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        # self.lifebar.paint(surface)

    def update(self):
        # any code here will happen every time the game loop updates
        # self.rect.x += 1

        x = self.rect.x + 138
        y = self.rect.y + 62
        self.gun_pos = (x, y)

        if self.bullets is not None:
            for bullet in self.bullets:
                bullet.update()

        self.hp = min(self.hp, self.hp_full)
        self.load = min(self.load, self.load_full)
        self.fuel = min(self.fuel, self.fuel_full)

        if self.fuel <= 0:
            self.speed_up = False
        if self.speed_up:
            self.fuel -= 1
            self.speed = self.speed_limit
        else:
            self.speed = int(self.speed_limit / 2)

    def jump(self):
        self.speed_up = False if self.speed_up else True

    def move(self, direction):
        if direction == "up":
            self.rect.y -= self.speed
        if direction == "down":
            self.rect.y += self.speed
        if direction == "left":
            self.rect.x -= self.speed
        if direction == "right":
            self.rect.x += self.speed

        if self.rect.x > WIDTH - 150:
            self.rect.x = WIDTH - 150
        if self.rect.x < -50:
            self.rect.x = -50
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > HEIGHT:
            self.rect.y = HEIGHT


class Enemy(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, image=enemy_img, speed=2, hp=1):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)

        # create a plain rectangle for the sprite image
        self.image = image
        self.image.set_colorkey(BLACK)

        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # self.mask = pygame.mask.from_surface(self.image)

        # center the sprite on the screen
        x = random.randint(int(WIDTH/2), WIDTH)
        y = random.randint(100, HEIGHT)
        self.rect.center = (x, y)

        # enemy's speed
        self.speed = speed

        # amo
        x = self.rect.x + 15
        y = self.rect.y + 95
        self.gun_pos = (x, y)

        self.bullets = pygame.sprite.Group()

        # HP
        self.hp = hp
        self.hp_full = hp
        self.lifebar = Lifebar(self)

    def update(self):
        x = self.rect.x + 15
        y = self.rect.y + 95
        self.gun_pos = (x, y)

        self.ai_movement()
        if self.bullets is not None:
            for bullet in self.bullets:
                bullet.update()

    def ai_movement(self):
        self.rect.x -= 1
        x = random.randint(0, 1000)
        if x < 10:
            bullet = Bullet(self, -1)
            self.bullets.add(bullet)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

        self.lifebar.paint(surface)


class Boss(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, image=boss_img, speed=2, direction=1, hp=20):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)

        # create a plain rectangle for the sprite image
        self.image = image
        self.image.set_colorkey(BLACK)

        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # self.mask = pygame.mask.from_surface(self.image)

        # center the sprite on the screen

        self.rect.center = (1600, 500)

        # enemy's spped
        self.speed = speed
        self.direction = direction

        # amo
        self.gun_pos = None

        self.bullets = pygame.sprite.Group()

        # hp
        self.hp = hp
        self.hp_full = hp

        self.lifebar = Lifebar(self)

    def update(self):
        x = self.rect.x + 15
        y = self.rect.y + 235
        self.gun_pos = (x, y)

        self.ai_movement()
        if self.bullets is not None:
            for bullet in self.bullets:
                bullet.update()

    def ai_movement(self):

        x = random.randint(0, 1000)

        if x < 20:
            self.direction *= -1

        if 0 <= self.rect.y <= HEIGHT:
            self.rect.y += self.direction * self.speed
        else:
            if self.rect.y < 0:
                self.rect.y = HEIGHT
            else:
                self.rect.y = 0


        if x < 20:
            bullet = Bullet(self, -1)
            self.bullets.add(bullet)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

        self.lifebar.paint(surface)


class Bullet(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, owner, direction=1):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)

        # create a plain rectangle for the sprite image
        if direction == 1:
            self.image = bullet_img
        else:
            self.image = enemy_bullet_img
        self.image.set_colorkey(BLACK)

        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # self.mask = pygame.mask.from_surface(self.image)

        # center the sprite on the screen
        self.owner = owner

        self.rect.center = self.owner.gun_pos

        # movement
        self.speed = 3
        self.direction = direction

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x > WIDTH:
            self.kill()


class Lifebar(pygame.sprite.Sprite):

    def __init__(self, owner):
        pygame.sprite.Sprite.__init__(self)

        self.owner = owner

    def paint(self, surface):

        if self.owner.hp_full < 3:
            return

        percent = self.owner.hp / self.owner.hp_full * 1.0
        pygame.draw.rect(surface, (0, 0, 0), (self.owner.rect.x-20, self.owner.rect.y-30, self.owner.rect.width - 2, 5))
        if percent < 0.3:
            color = RED
        elif percent > 0.8:
            color = GREEN
        else:
            color = YELLOW
        pygame.draw.rect(surface, color,
                         (self.owner.rect.x-20, self.owner.rect.y-30, int(self.owner.rect.width * percent), 5))


class Prop(pygame.sprite.Sprite):
    def __init__(self,):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)

        # create a plain rectangle for the sprite image
        event_id = random.randint(1, 3)
        self.event_id = event_id
        try:
            self.image = Event_img[event_id]
        except KeyError:
            raise KeyError
        self.image.set_colorkey(BLACK)

        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # self.mask = pygame.mask.from_surface(self.image)

        # center the sprite on the screend
        x = random.randint(0, WIDTH)
        y = random.randint(100, HEIGHT)
        self.rect.center = (x, y)

        # event_id

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
