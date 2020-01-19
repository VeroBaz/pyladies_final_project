# Graphics for the game

import pygame

# Background - image has to be saved in a directory called "images"
BACKGROUND = pygame.image.load("images/bg.png")

# Character graphics - images have to be saved in a directory called "images"

# Character - walking
walk_original = [pygame.image.load("images/2_WALK_000.png"), pygame.image.load("images/2_WALK_001.png"),
                 pygame.image.load("images/2_WALK_002.png"), pygame.image.load("images/2_WALK_003.png"),
                 pygame.image.load("images/2_WALK_004.png")]

# Character - jumping
jump_original = [pygame.image.load("images/4_JUMP_000.png"), pygame.image.load("images/4_JUMP_001.png"),
                 pygame.image.load("images/4_JUMP_002.png"), pygame.image.load("images/4_JUMP_003.png"),
                 pygame.image.load("images/4_JUMP_004.png")]

# Character - standing
standing_original = [pygame.image.load("images/standing.png")]

# Monsters graphics
monsters_original = [pygame.image.load("images/monster_1.png"), pygame.image.load("images/monster_2.png"),
                     pygame.image.load("images/monster_3.png"), pygame.image.load("images/monster_4.png"),
                     pygame.image.load("images/monster_5.png"), pygame.image.load("images/monster_6.png"),
                     pygame.image.load("images/monster_7.png"), pygame.image.load("images/monster_8.png")]

# Platform graphics
platform_images_original = [pygame.image.load("images/platform_1.png"),
                            pygame.image.load("images/platform_2.png")]

# Coin graphics
coin_original = [pygame.image.load("images/coin.png")]

# Resize the images

walk_right = []
jump_right = []
standing_right = []
platform_images = []
coin_image = []
monsters_images = []


def modify_character_size(original_images, resized_images, divisor):
    for image in original_images:
        resized_images.append(pygame.transform.scale(image,(int(image.get_width() / divisor),
                                                            int(image.get_height() / divisor))))


modify_character_size(walk_original, walk_right, 4.5)
modify_character_size(jump_original, jump_right, 4.5)
modify_character_size(standing_original, standing_right, 4.5)
modify_character_size(platform_images_original, platform_images, 5)
modify_character_size(coin_original, coin_image, 16)
modify_character_size(monsters_original, monsters_images, 6)

# Get images for left movements

walk_left = []
jump_left = []
standing_left = []


def flip_image_horizontally(right_images, left_images):
    for image in right_images:
        left_images.append(pygame.transform.flip(image, True, False))


flip_image_horizontally(walk_right, walk_left)
flip_image_horizontally(jump_right, jump_left)
flip_image_horizontally(standing_right, standing_left)
