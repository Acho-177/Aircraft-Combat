import pygame
import os
import random
from resource import *

# object class


class Player(pygame.sprite.Sprite):
    # sprite for the Player
    # default construction: img=player_img, hp=10, speed=2, load=1000, fuel=5000, speed_limit=5
    def __init__(self, img=player_img, hp=10, speed=2, load=1000, fuel=5000, speed_limit=5):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)

        # create a plain rectangle for the sprite image
        self.image = img
        #self.image.set_colorkey(BLACK)

        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()

        # center the sprite on the screen
        self.rect.center = (self.rect.width / 2, HEIGHT / 2)

        # player's speed
        self.default_speed = speed
        self.speed_limit = speed_limit
        self.speed = speed

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

        gun_x = self.rect.x + 138
        gun_y = self.rect.y + 62
        self.gun_pos = (gun_x, gun_y)

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
            self.speed = self.default_speed

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
    # default construction: image=enemy_img, speed=2, hp=1
    def __init__(self, image=enemy_img, speed=2, hp=1):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)

        # create a plain rectangle for the sprite image
        self.image = image
        #self.image.set_colorkey(BLACK)

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
        #self.image.set_colorkey(BLACK)

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
        gun_x = self.rect.x + 15
        gun_y = self.rect.y + 235
        self.gun_pos = (gun_x, gun_y)

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
        #self.image.set_colorkey(BLACK)

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