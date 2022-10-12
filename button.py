import pygame
from resource import *


class Button(object):
    def __init__(self, text, color, x, y, screen, font):
        self.surface = font.render(text, True, color)

        self.color = color
        self.text = text
        self.font = font

        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()

        self.screen = screen

        self.x = x
        self.y = y
        '''if 'centered_x' in kwargs and kwargs['centered_x']:
            self.x = display_width // 2 - self.WIDTH // 2
        else:
            self.x = x

        if 'centered_y' in kwargs and kwargs['cenntered_y']:
            self.y = display_height // 2 - self.HEIGHT // 2
        else:
            self.y = y'''

    def display(self):
        self.screen.blit(self.surface, (self.x, self.y))

    def check_focus(self, position):
        x_match = self.x < position[0] < self.x + self.WIDTH
        y_match = self.y < position[1] < self.y + self.HEIGHT

        if x_match and y_match:
            return True
        else:
            return False

    def hover_switch(self, position):
        if self.check_focus(position):
            self.surface = self.font.render(self.text, True, GREY)
            return True
        else:
            self.surface = self.font.render(self.text, True, self.color)
            return False
