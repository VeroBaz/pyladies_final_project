# Game settings

import pygame
from graphics import *

TITLE = "Jumping Wizard"
WIDTH = 1200
HEIGHT = 675
FPS = 60
FONT_NAME = "comicsansms"
HIGH_SCORE_FILE = "highscore.txt"

# Player properties
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.9
PLAYER_JUMP = 18

# Platforms
PLATFORM_LIST = [(WIDTH - 380, HEIGHT - 320, platform_images[1]),
                 (WIDTH - 1040, HEIGHT - 270, platform_images[1]),
                 (WIDTH - 650, HEIGHT - 505),
                 (WIDTH - 690, HEIGHT - 245),
                 (WIDTH - 850, HEIGHT - 140, platform_images[1]),
                 (WIDTH - 280, HEIGHT - 185),
                 (WIDTH - 190, HEIGHT - 420, platform_images[1]),
                 (WIDTH - 370, HEIGHT - 560, platform_images[1]),
                 (WIDTH - 855, HEIGHT - 400, platform_images[1])]

# Positions of coins and monsters

coins_monsters_positions = []


def get_positions_for_coins_and_monsters():
    for item in PLATFORM_LIST:
        if len(item) > 2:
            x = item[0] + 15
            y = item[1] - 40
            position = (x, y)
            coins_monsters_positions.append(position)
        else:
            x = item[0] + 70
            y = item[1] - 40
            position = (x, y)
            coins_monsters_positions.append(position)


get_positions_for_coins_and_monsters()

# Define colors
WHITE = (255, 255, 255)
