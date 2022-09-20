import math
import sys
import random
import pygame
import time
from pygame import mixer

pygame.init()

# Constants

SCREEN_WIDTH = 470
SCREEN_HEIGHT = 600
MIDDLE_X = 210
RASEN_FIRST_Y = 490
PLAYER_Y = 545
SPEED = 20
ZOMBIE_COORDINATES = [(80, 0), (195, 41), (335, 25), (70, 100), (220, 123), (375, 87), (355, 175), (140, 201)]
SCRORE_X = 10
SCRORE_Y = 500
TIMER_X = 170
TIMER_Y = 0
GAME_TIME = 60000
ZOMBIE_SPEED = 10

# Variables
timer = 0
change_hole_zombie = True
zombie_co_ind = 0
old_zombie_co_ind = 8

# Setup assets
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load('background.png')
zombie = pygame.image.load('zombie.png')
explosion = pygame.image.load('nuclear-explosion.png')
naruto = pygame.image.load('naruto.jpg')
layer1 = pygame.image.load("background1.png")
layer2 = pygame.image.load('background2.png')
layer3 = pygame.image.load('background3.png')
mask = pygame.image.load('mask.png')

# Explode
explosion_x = -100
explosion_y = -100


# Bullets
rasenShurikenImg = pygame.image.load('rasen_shuriken.png')
rasenShurikenX = MIDDLE_X
rasenShurikenY = RASEN_FIRST_Y
rasenShuriken_changed_x = 0
rasenShuriken_changed_y = -SPEED
rasen_state = "ready"

# Zombies
zombie_state = "change_hole"
zombie_x, zombie_y = ZOMBIE_COORDINATES[0]
zombie_y_anim = zombie_y

# Sounds
mixer.init()
mixer.music.load("BackgroundTheme.wav")
mixer.music.play(-1)


def fire_rasen_shuriken(x, y):
    global rasen_state
    rasen_state = "fire"
    screen.blit(rasenShurikenImg, (x, y))


def zombie_ins(random_inx):
    global zombie_x, zombie_y, zombie_y_anim, zombie_state
    zombie_x, zombie_y = ZOMBIE_COORDINATES[random_inx]
    if zombie_state == "change_hole":
        zombie_y_anim = zombie_y + 60
        zombie_state = "appear"
    elif zombie_state == "appear":
        zombie_y_anim -= ZOMBIE_SPEED
        if zombie_y_anim <= zombie_y:
            zombie_state = "idle"
    elif zombie_state == "disappear":
        zombie_y_anim += ZOMBIE_SPEED
    else:
        zombie_y_anim = zombie_y
    screen.blit(zombie, (zombie_x, zombie_y_anim))
    screen.blit(mask, (0, SCREEN_HEIGHT - 10 - 292))
    if (random_inx < 3):
        screen.blit(layer1, (0, 10))
    elif (random_inx < 6):
        screen.blit(layer2, (0, 10))
    else:
        screen.blit(layer3, (0, 10))



def is_collision(rasenX, rasenY, zomX, zomY):
    distance = math.sqrt(math.pow(rasenX - zomX, 2) + (math.pow(rasenY - zomY, 2)))

    if distance < 64:
        hit_sound = mixer.Sound("Punch_Hit_Sound_Effect.wav")
        hit_sound.play()
        #screen.blit(zombie, (-100, -100))
        return True
    else:
        return False


# Score

score_value = 0
miss_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    miss = font.render("Miss : " + str(miss_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
    screen.blit(miss, (x, y + 30))


def show_time(time, x, y):
    fnt_time = pygame.font.Font('freesansbold.ttf', 20)
    left_time = fnt_time.render("Left time : " + str(time) + " s", True, (255, 255, 255))
    screen.blit(left_time, (x, y))


# Game loop
running = True
is_kill_zombie = False
timer_explode = time.time()

def play():
    global zombie_co_ind
    global change_hole_zombie
    global old_zombie_co_ind
    global rasen_state
    global timer
    global rasenShuriken_changed_y
    global rasenShuriken_changed_x
    global rasenShurikenX
    global rasenShurikenY
    global is_kill_zombie
    global timer_explode
    global score_value
    global zombie_y_anim
    global zombie_state

    pygame.display.set_caption("Whack the Zom")
    static_time = pygame.time.get_ticks()
    while running:
        clock = pygame.time.Clock()
        screen.fill((204, 152, 102, 255))
        screen.blit(background, (0, 10))
        screen.blit(naruto, (MIDDLE_X, PLAYER_Y))

        if is_kill_zombie:
            screen.blit(explosion, (explosion_x, explosion_y))
        else:
            zombie_ins(zombie_co_ind)

        if time.time() - timer >= 0.8 and not is_kill_zombie:
            zombie_state = "disappear"

        if time.time() - timer > 1:
            change_hole_zombie = True
            zombie_state = "change_hole"

        if (time.time() - timer_explode)*100 > 25:
            is_kill_zombie = False
            if change_hole_zombie:
                timer = time.time()
                zombie_co_ind = random.randint(0, 7)
                while zombie_co_ind == old_zombie_co_ind:
                    zombie_co_ind = random.randint(0, 7)
                old_zombie_co_ind = zombie_co_ind
                change_hole_zombie = False

        # Rasen suriken
        if rasen_state == "fire":
            rasenShurikenX += rasenShuriken_changed_x
            rasenShurikenY += rasenShuriken_changed_y
            fire_rasen_shuriken(rasenShurikenX, rasenShurikenY)
        else:
            rasenShurikenX = MIDDLE_X
            rasenShurikenY = RASEN_FIRST_Y
            screen.blit(rasenShurikenImg, (rasenShurikenX, rasenShurikenY))

        if rasenShurikenY <= 0 or rasenShurikenX >= SCREEN_WIDTH or rasenShurikenX <= 0:
            global miss_value
            miss_value += 1
            rasen_state = "ready"

        # Collisions
        if is_collision(rasenShurikenX, rasenShurikenY, zombie_x, zombie_y):
            is_kill_zombie = True
            change_hole_zombie = True
            explosion_x = zombie_x
            explosion_y = zombie_y

            screen.blit(explosion, (explosion_x, explosion_y))
            screen.blit(zombie, (-90, -90))
            timer_explode = time.time()
            score_value += 1
            rasen_state = "ready"

        # Event detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                distance_x = mouse_x - MIDDLE_X
                distance_y = mouse_y - PLAYER_Y
                angle = math.atan2(distance_y, distance_x)
                speed_x = SPEED * math.cos(angle) - 0.2
                speed_y = SPEED * math.sin(angle)
                rasenShuriken_changed_x = speed_x
                rasenShuriken_changed_y = speed_y
                fire_rasen_shuriken(rasenShurikenX, rasenShurikenY)

        current_time = -static_time + pygame.time.get_ticks()
        left_time = GAME_TIME - current_time
        if left_time <= 1000:
            end_game()
        left_time /= 1000
        show_time(left_time, TIMER_X, TIMER_Y)
        show_score(SCRORE_X, SCRORE_Y)
        pygame.display.update()
        clock.tick(60)


def end_game():
    pygame.display.set_caption("Game Finished")
    global score_value
    global miss_value
    global rasen_state
    while True:
        screen.fill((204, 152, 102, 255))
        play_button = font.render("PLAY AGAIN", True, (100, 100, 100))
        score = font.render("Your score: " + str(score_value), True, (100, 100, 100))
        miss = font.render("Your misses: " + str(miss_value), True, (100, 100, 100))
        screen.blit(play_button, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 20))
        screen.blit(score, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 40))
        screen.blit(miss, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (SCREEN_WIDTH / 2 - 100) < mouse_x < (SCREEN_WIDTH / 2 + 80):
                    if (SCREEN_HEIGHT / 2 - 20) < mouse_y < SCREEN_HEIGHT / 2 + 30:
                        score_value = 0
                        miss_value = 0
                        rasen_state = "ready"
                        play()

        pygame.display.update()


def main_menu():
    pygame.display.set_caption("Menu")

    while True:
        screen.fill((204, 152, 102, 255))
        play_button = font.render("PLAY", True, (255, 255, 255))
        screen.blit(play_button, (SCREEN_WIDTH / 2 - 40, SCREEN_HEIGHT / 2 - 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (SCREEN_WIDTH / 2 - 40) < mouse_x < (SCREEN_WIDTH / 2 + 60):
                    if (SCREEN_HEIGHT / 2 - 20) < mouse_y < SCREEN_HEIGHT / 2 + 30:
                        play()

        pygame.display.update()


main_menu()
