import math
import sys
import random
import pygame
import time

pygame.init()

# Constants

SCREEN_WIDTH = 470
SCREEN_HEIGHT = 600
MIDDLE_X = 210
RASEN_FIRST_Y = 490
PLAYER_Y = 545
SPEED = 2
ZOMBIE_COORDINATES = [(80, 0), (195, 41), (335, 25), (70, 100), (220, 123), (375, 87), (355, 175), (140, 201)]
SCRORE_X = 10
SCRORE_Y = 500

# Variables
timer = 0
change_hole_zombie = True
zombie_co_ind = 0
old_zombie_co_ind = 8

# Setup assets
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load('background.png')
zombie = pygame.image.load('zombie.png')
naruto = pygame.image.load('naruto.jpg')

# Caption and icon
pygame.display.set_caption("Whack the Zom")

# Bullets
rasenShurikenImg = pygame.image.load('rasen_shuriken.png')
rasenShurikenX = MIDDLE_X
rasenShurikenY = RASEN_FIRST_Y
rasenShuriken_changed_x = 0
rasenShuriken_changed_y = -SPEED
rasen_state = "ready"

# Zombies

zombie_x, zombie_y = ZOMBIE_COORDINATES[0]


def fire_rasen_shuriken(x, y):
    global rasen_state
    rasen_state = "fire"

    screen.blit(rasenShurikenImg, (x, y))


def zombie_ins(random_inx):
    global zombie_x, zombie_y
    zombie_x, zombie_y = ZOMBIE_COORDINATES[random_inx]
    screen.blit(zombie, (zombie_x, zombie_y))


def is_collision(rasenX, rasenY, zomX, zomY):
    distance = math.sqrt(math.pow(rasenX - zomX, 2) + (math.pow(rasenY - zomY, 2)))
    if distance < 64:
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
    screen.blit(miss, (x, y+30))

# Game loop
running = True

while running:

    screen.fill((204, 152, 102, 255))
    screen.blit(background, (0, 10))
    screen.blit(naruto, (MIDDLE_X, PLAYER_Y))
    zombie_ins(zombie_co_ind)
    if change_hole_zombie:
        timer = time.time()
        zombie_co_ind = random.randint(0, 7)
        while zombie_co_ind == old_zombie_co_ind:
            zombie_co_ind = random.randint(0, 7)
        old_zombie_co_ind = zombie_co_ind
        change_hole_zombie = False

    if time.time() - timer > 2:
        change_hole_zombie = True

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
        miss_value += 1
        rasen_state = "ready"

    # Collisions
    if is_collision(rasenShurikenX, rasenShurikenY, zombie_x, zombie_y):
        score_value  += 1
        change_hole_zombie = True
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
    show_score(SCRORE_X, SCRORE_Y)
    pygame.display.update()