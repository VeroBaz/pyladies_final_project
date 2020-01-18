# Game settings

import pygame
from graphics import *

TITLE = "Jumping Wizard"
WIDTH = 1200
HEIGHT = 675
FPS = 60
FONT_NAME = "arial"
HIGHSCORE_FILE = "highscore.txt"

# Player properties
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = 17

# Platforms
PLATFORM_LIST = [(WIDTH - 380, HEIGHT - 320, platform_images[1]),
                 (WIDTH - 1040, HEIGHT - 270, platform_images[1]),
                 (WIDTH - 650, HEIGHT - 520),
                 (WIDTH - 730, HEIGHT - 280),
                 (WIDTH - 850, HEIGHT - 140, platform_images[1]),
                 (WIDTH - 280, HEIGHT - 185),
                 (WIDTH - 170, HEIGHT - 420, platform_images[1]),
                 (WIDTH - 370, HEIGHT - 570, platform_images[1]),
                 (WIDTH - 870, HEIGHT - 420, platform_images[1])]

# Location of coins

coins_locations = []

def get_location_for_coins():
    for item in PLATFORM_LIST:
        if len(item) > 2:
            x = item[0] + 25
            y = item[1] - 45
            location = (x, y)
            coins_locations.append(location)
        else:
            x = item[0] + 90
            y = item[1] - 45
            location = (x, y)
            coins_locations.append(location)
    return coins_locations

get_location_for_coins()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (18, 65, 46)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (0, 155, 155)
BROWN = (195, 128, 99)
VIOLET = (126, 101, 130)
GREY = (47, 79, 79)