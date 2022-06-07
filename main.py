import pygame
import random
import time
import sys

from pygame import KEYDOWN, K_SPACE, K_a, KEYUP, QUIT, K_ESCAPE


from object import *


WIDTH = 1920  # 游戏窗口的宽度
HEIGHT = 1200 # 游戏窗口的高度
FPS = 144 # 帧率

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (144, 238, 144)
BLUE = (0, 0, 255)
YELLOW = (255, 215, 0)
GREY = (28, 28, 28)

# resource
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
bg_img = pygame.image.load(os.path.join(img_folder, 'bg.jpg'))
bg_img = pygame.transform.scale(bg_img, (1920, 1200))

hpBar_img = pygame.image.load(os.path.join(img_folder, 'bar1.png'))
hpBar_img = pygame.transform.rotozoom(hpBar_img, 0, 0.8)

music_folder = os.path.join(game_folder, 'music')

count = 0
BOSS = False
switch = True
boss_gap = 3000
start = time.time()
score = 0

# game setting
winPoint = 25
NormalEnemyCreatePossibility = 3
NormalPropCreatePossibility = 1
prop_hp = 2
prop_load = 20
prop_fuel = 500

# initialize game
pygame.init()
pygame.mixer.init()  # 声音初始化

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1")
clock = pygame.time.Clock()


# initialize player and other groups
player = Player()
enemies = pygame.sprite.Group()
all_boss = pygame.sprite.Group()
props = pygame.sprite.Group()


def main():

    global player, BOSS, count, score, switch
    BOSS = False
    pygame.event.clear()
    player.reset()
    # initialize pygame and create window
    # show gamestart screen
    game_start()

    count = 0  # reset time counter
    switch = True  # turn the bgm switch trigger to True

    #  run the game
    run()

    # quit
    terminate()

    return


#  check game quit
def check_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.event.clear()
            terminate()
    return


# check speed up
def check_jump():
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]:
        pygame.event.clear()
        return True


# check fire(left mouse button click or key q)
def check_shot():

    state = pygame.mouse.get_pressed()
    pressed = pygame.key.get_pressed()
    res = state[0] or pressed[pygame.K_q]
    pygame.event.clear()
    return res


# check player moving
def check_move():
    pressed = pygame.key.get_pressed()
    res = None
    if pressed[pygame.K_w]:
        res = "up"
    elif pressed[pygame.K_a]:
        res = "left"
    elif pressed[pygame.K_s]:
        res = "down"
    elif pressed[pygame.K_d]:
        res = "right"

    pygame.event.clear()
    return res


# check win
def check_win():
    if score > winPoint:
        return True


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


# check Space press
def checkForKeyPress():

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_SPACE:
        return True


# check collision between objects
def check_collision():

    global BOSS, score, switch
    #  get all bullets from enemies (include boss)
    all_bullets = getEnemyBullets()

    #  check for the collision between player's bullet and enemies'(include boss)
    for bullet in player.bullets:
        for enemy in enemies:
            if pygame.sprite.collide_rect_ratio(0.4)(bullet, enemy):
                bullet.kill()
                enemy.hp -= 1
                if enemy.hp <= 0:
                    enemy.kill()
                    score += 1

        for boss in all_boss:
            if pygame.sprite.collide_rect_ratio(0.4)(bullet, boss):
                bullet.kill()
                boss.hp -= 1
                if boss.hp <= 0:
                    boss.kill()
                    score += 10

                    BOSS = False
                    switch = True

    #  check for the collision between enemies' bullet and player
    for enemy in enemies:
        if pygame.sprite.collide_rect_ratio(0.2)(player, enemy):
            enemy.kill()
            score += 1

            player.hp -= 1
        for bullet in enemy.bullets:
            if pygame.sprite.collide_rect_ratio(0.2)(player, bullet):
                bullet.kill()
                player.hp -= 1

    for enemy in all_boss:
        if pygame.sprite.collide_rect_ratio(0.2)(player, enemy):
            enemy.hp -= 1
            player.hp -= 1
            if enemy.hp <= 0:
                enemy.kill()
                score += 10

                BOSS = False
                switch = True

        for bullet in enemy.bullets:
            if pygame.sprite.collide_rect_ratio(0.2)(player, bullet):
                bullet.kill()
                player.hp -= 1

    #  check for the collision between bullets
    for bullet in player.bullets:
        for enemy_b in all_bullets:
            if pygame.sprite.collide_rect_ratio(1)(bullet, enemy_b):
                bullet.kill()
                enemy_b.kill()

    # check for the collision between player and prop
    for prop in props:
        if pygame.sprite.collide_rect_ratio(1)(player, prop):
            prop_event(player, prop.event_id)
            prop.kill()

    return


# create enemy
def create_enemy():
    global BOSS, all_boss

    x = random.randint(0, 1000)

    if x < NormalEnemyCreatePossibility and not BOSS:
        enemy = Enemy()
        enemies.add(enemy)

    if count % boss_gap == 0 and not BOSS and count != 0:
        boss = Boss()
        BOSS = True
        all_boss.add(boss)

        pygame.mixer.music.load(os.path.join(music_folder, 'boss_music.mp3'))
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.01)


# create prop
def create_prop():
    x = random.randint(0, 1000)
    if x < NormalPropCreatePossibility:
        prop = Prop()
        props.add(prop)


# process prop event
def prop_event(target, event_id):

    # process event
    if event_id == 1:
        target.hp += prop_hp
    elif event_id == 2:
        target.load += prop_load
    elif event_id == 3:
        target.fuel += prop_fuel

    player.update()


# get all bullets from enemies
def getEnemyBullets():
    all_bullets = pygame.sprite.Group()

    for enemy in enemies:
        for bullet in enemy.bullets:
            all_bullets.add(bullet)

    for boss in all_boss:
        for bullet in boss.bullets:
            all_bullets.add(bullet)

    return all_bullets


# get all bullets(enemies and player)
def getAllBullets():
    all_bullets = pygame.sprite.Group()

    for enemy in enemies:
        for bullet in enemy.bullets:
            all_bullets.add(bullet)

    for boss in all_boss:
        for bullet in boss.bullets:
            all_bullets.add(bullet)

    for bullet in player.bullets:
        all_bullets.add(bullet)

    return all_bullets


# game start screen
def game_start():

    # play start bgm
    pygame.mixer.music.load(os.path.join(music_folder, 'start_music.mp3'))
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.2)

    '''screen.blit(bg_img, (0, 0))

    myFont = pygame.font.Font(None, 80)
    loadImage = myFont.render("Press SPACE to Start", True, WHITE)
    screen.blit(loadImage, (650, 1000))

    pygame.display.update()
    pygame.time.wait(1000)

    pygame.event.clear()

    while True:
        if checkForKeyPress():
            break'''

    screen.blit(bg_img, (0, 0))

    start_x = 200
    start_y = 400
    gap = 100
    length = 200

    startFont = pygame.font.Font(None, 80)

    startImage = startFont.render("Start", True, WHITE)
    screen.blit(startImage, (start_x, start_y + 0 * gap))

    startImage = startFont.render("Setting", True, WHITE)
    screen.blit(startImage, (start_x, start_y + 1 * gap))

    startImage = startFont.render("Exit", True, WHITE)
    screen.blit(startImage, (start_x, start_y + 2 * gap))

    pygame.display.update()
    pygame.event.clear()

    while True:
        check_quit()

        loc = check_click()
        if loc is not None:
            if loc[0] in range(start_x, start_x + length) and loc[1] in range(400, 450):  # start
                return
            if loc[0] in range(start_x, start_x + length) and loc[1] in range(480, 550):  # setting
                player_setting()
                game_start()
            if loc[0] in range(start_x, start_x + length) and loc[1] in range(560, 650):  # exit
                terminate()


# player setting (level up)
def player_setting():

    screen.blit(bg_img, (0, 0))
    myFont = pygame.font.Font(None, 80)
    loadImage = myFont.render("Load", True, WHITE)
    screen.blit(loadImage, (200, 400))

    loadImage = myFont.render("Back", True, WHITE)
    screen.blit(loadImage, (200, 500))

    pygame.display.update()
    pygame.event.clear()

    while True:
        if check_quit():
            terminate()

        loc = check_click()
        if loc is not None:
            if loc[0] in range(200, 400) and loc[1] in range(400, 500):  # loading player
                load()
                return
            if loc[0] in range(200, 400) and loc[1] in range(500, 600):  # back
                return


# game over
def game_over():
    check_quit()

    # play game over music
    pygame.mixer.music.load(os.path.join(music_folder, 'gameover_music.mp3'))
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.01)

    # draw game over
    gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WIDTH / 2, 10)
    overRect.midtop = (WIDTH / 2, gameRect.height + 10 + 25)

    screen.blit(gameSurf, gameRect)
    screen.blit(overSurf, overRect)

    drawPressKeyMsg()

    pygame.display.update()
    pygame.time.wait(1000)

    while True:
        if checkForKeyPress():
            return


# game win
def game_win():

    # draw background
    screen.blit(bg_img, (0, 0))

    myFont = pygame.font.Font(None, 80)
    loadImage = myFont.render("YOU WIN. Press SPACE to Start", True, WHITE)
    screen.blit(loadImage, (550, 1000))

    player.draw(screen)

    pygame.display.update()
    pygame.time.wait(1000)

    while True:
        if checkForKeyPress():
            return


# process pause
def pause():

    start_x = 700
    start_y = 500
    gap = 100
    length = 600

    myFont = pygame.font.Font(None, 80)

    pauseImage = myFont.render("Back to main Menu", True, WHITE)
    screen.blit(pauseImage, (start_x, start_y))

    pauseImage = myFont.render("Back to Game", True, WHITE)
    screen.blit(pauseImage, (start_x, start_y + gap))

    pygame.display.update()

    while True:
        check_quit()

        loc = check_click()
        if loc is not None:
            if loc[0] in range(start_x, start_x + length) and loc[1] in range(500, 590):  # Back to main Menu
                save()
                main()
                terminate()

            if loc[0] in range(start_x, start_x + length) and loc[1] in range(590, 680):  # Back to Game
                return


# close the game
def terminate():
    save()
    pygame.quit()
    sys.exit()


def run():

    global screen, player, enemies, clock, count, start, switch, score

    # clear up
    props.empty()
    enemies.empty()
    all_boss.empty()
    pygame.event.clear()

    # reset score counter
    score = 0

    while True:

        clock.tick(FPS)

        # check switch music
        if switch:
            pygame.mixer.music.load(os.path.join(music_folder, 'bg_music.mp3'))
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.03)
            switch = False

        # Process input (events)
        check_quit()

        # check win
        if check_win():
            game_win()
            save()
            main()
            terminate()

        # check jump
        if check_jump():
            player.jump()

        # check shot
        if check_shot() and count % 15 == 0 and player.load > 0:
            bullet = Bullet(player)
            player.bullets.add(bullet)
            player.load -= 1

        # check pause
        if check_esc():
            pause()

        # player moving
        player.move(check_move())

        # randomly create enemies and props
        create_enemy()
        create_prop()

        # check collision
        check_collision()

        # check game over
        if player.hp < 0:
            game_over()
            save()
            main()
            terminate()

        # Update
        player.update()
        enemies.update()
        all_boss.update()
        props.update()

        #  get message that need to present

        fpsImage = drawFPS()
        scoreImage = drawScore()

        # Draw / Render
        screen.blit(bg_img, (0, 0))

        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for boss in all_boss:
            boss.draw(screen)
        for prop in props:
            prop.draw(screen)

        getAllBullets().draw(screen)
        drawHUD(screen)
        # screen.blit(fpsImage, (0, 0))
        screen.blit(scoreImage, (1700, 0))

        pygame.display.flip()


def drawFPS():
    global count
    count += 1
    now = time.time()
    elapse = now - start
    fpsfont = pygame.font.Font(None, 25)
    fps = count / elapse if elapse != 0 else 0

    fpsImage = fpsfont.render("FPS: " + str(fps), True, WHITE)
    return fpsImage


def drawScore():
    scoreFont = pygame.font.Font(None, 50)
    scoreImage = scoreFont.render("Score: " + str(score), True, WHITE)
    return scoreImage


def drawHUD(surface):
    surface.blit(player.image, (50, 1050))

    def set_color(perc):
        if perc < 0.5:
            res = RED
        elif perc > 0.9:
            res = GREEN
        else:
            res = YELLOW
        return res

    bg_color = BLACK

    # Draw Hp information
    # surface.blit(hpBar_img, (192, 1037))

    hpFont = pygame.font.Font(None, 35)
    hpImage = hpFont.render("   Hp: ", True, WHITE)
    screen.blit(hpImage, (155, 1070))

    percent = player.hp / player.hp_full * 1.0
    pygame.draw.rect(surface, bg_color, (250, 1080, 15 * player.hp_full, 8))
    color = set_color(percent)
    pygame.draw.rect(surface, color,
                     (250, 1080, 15 * player.hp * percent + 10, 8))

    # Draw Amo information
    amoFont = pygame.font.Font(None, 35)
    amoImage = amoFont.render("Amo: ", True, WHITE)
    screen.blit(amoImage, (155, 1100))

    percent = player.load / player.load_full * 1.0
    pygame.draw.rect(surface, bg_color, (250, 1110, 0.3 * player.load_full, 10))
    color = set_color(percent)
    pygame.draw.rect(surface, color,
                     (250, 1110, 0.3 * player.load * percent, 10))

    # Draw fuel information
    fuelFont = pygame.font.Font(None, 35)
    fuelImage = amoFont.render("Fuel: ", True, WHITE)
    screen.blit(fuelImage, (155, 1130))

    percent = player.fuel / player.fuel_full * 1.0
    pygame.draw.rect(surface, bg_color, (250, 1140, 0.02 * (player.fuel_full - 2), 10))
    color = set_color(percent)
    pygame.draw.rect(surface, color,
                     (250, 1140, 0.02 * player.fuel * percent, 10))


def drawPressKeyMsg():
    myfont = pygame.font.Font(None, 80)
    loadImage = myfont.render("Press SPACE to Continue", True, WHITE)
    screen.blit(loadImage, (650, 1000))


def load(filename="data.txt"):

    with open(filename, "r") as file:
        data = file.readlines()
    for line in data:
        line = int(line.strip('\n'))

    player.hp_full = int(data[0])
    player.hp = int(data[0])
    player.load_full = int(data[1])
    player.fuel_full = int(data[2])


def save(filename="data.txt"):
    data = None
    with open(filename, "r") as file:
        data = file.readlines()
        for line in data:
            line = int(line.strip('\n'))
    file.close()

    with open(filename, "w") as file:
        file.write(str(player.hp_full) + '\n')
        file.write(str(player.load_full) + '\n')
        file.write(str(player.fuel_full) + '\n')
        file.write(str(player.speed_limit) + '\n')
        file.write(str(int(data[4]) + score) + '\n')


if __name__ == '__main__':
    main()
