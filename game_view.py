import pygame
import random
import time
import sys

from resource import *

from player import *
from button import *

# initialize game
pygame.init()  # initialize game structure
pygame.mixer.init()  # initialize music
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # set game screen 1920*1200 as default
pygame.display.set_caption("Air-Combat")
CLOCK = pygame.time.Clock()

# initialize player and groups
player = Player()
enemies = pygame.sprite.Group()
all_boss = pygame.sprite.Group()
props = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


def main():

    pygame.event.clear()
    player.reset()

    game_start()

    terminate()


START_MUSIC = "start_music.mp3"
BG_MUSIC = "bg_music.mp3"


def game_start():

    screen.blit(bg_img, (0, 0))

    # play start bgm
    try:
        pygame.mixer.music.load(os.path.join(music_folder, BG_MUSIC))
    except FileNotFoundError:
        print(START_MUSIC + " file not found!")

    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.2)

    buttons = []
    Font = pygame.font.Font(None, 80)
    start_button = Button("Start",     WHITE, 200, 400, screen, Font)
    shop_button = Button("Shop",       WHITE, 200, 500, screen, Font)
    setting_button = Button("Setting", WHITE, 200, 600, screen, Font)
    exit_button = Button("Exit",       WHITE, 200, 700, screen, Font)
    buttons.append(start_button)
    buttons.append(shop_button)
    buttons.append(setting_button)
    buttons.append(exit_button)

    for button in buttons:
        button.display()

    pygame.display.update()
    pygame.event.clear()

    while True:
        loc = check_click()

        if loc:
            if start_button.check_focus(loc):
                game_run()
            if shop_button.check_focus(loc):
                shop_page()
            if setting_button.check_focus(loc):
                setting_page()
            if exit_button.check_focus(loc):
                terminate()

        pos = pygame.mouse.get_pos()
        for button in buttons:
            button.hover_switch(pos)
            button.display()
        pygame.display.update()


#  check game quit
def check_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.event.clear()
            terminate()
    return


# check mouse click and return the clicked position
def check_click():

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            res = event.pos
            pygame.event.clear()
            return res
    return None


# check Esc click
def check_esc():
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        pygame.event.clear()
        return True


def game_run():
    terminate()


def shop_page():

    screen.blit(bg_img, (0, 0))
    startFont = pygame.font.Font(None, 80)

    startImage = startFont.render("EMPTY NOW", True, WHITE)
    screen.blit(startImage, (800, 500))

    #total_score = get_score()
    total_score = 0

    hpFont = pygame.font.Font(None, 80)
    hpImage = hpFont.render("   Score: " + str(int(total_score)), True, WHITE)
    screen.blit(hpImage, (100, 100))

    pygame.display.update()
    pygame.event.clear()

    while True:

        if check_quit():
            terminate()

        if check_esc():
            game_start()

        loc = check_click()
        if loc is not None:
            pass


def setting_page():
    terminate()


main()
