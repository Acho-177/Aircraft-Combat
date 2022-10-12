import pygame
from resource import *
import random

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