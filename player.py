import pygame
from resource import *
from lifebar import *


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