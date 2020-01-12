# Graphics for the game

import pygame

# Background - image has to be saved in a directory called "images"
BACKGROUND = pygame.image.load("images/bg.png")

# Character images - images have to be saved in a directory called "images"

#   Character - walking
walk_original = [pygame.image.load("images/2_WALK_000.png"), pygame.image.load("images/2_WALK_001.png"),
                 pygame.image.load("images/2_WALK_002.png"), pygame.image.load("images/2_WALK_003.png"),
                 pygame.image.load("images/2_WALK_004.png")]

# Character - running
run_original = [pygame.image.load("images/3_RUN_000.png"), pygame.image.load("images/3_RUN_001.png"),
                pygame.image.load("images/3_RUN_002.png"), pygame.image.load("images/3_RUN_003.png"),
                pygame.image.load("images/3_RUN_004.png")]

# Character - jumping
jump_original = [pygame.image.load("images/4_JUMP_000.png"), pygame.image.load("images/4_JUMP_001.png"),
                 pygame.image.load("images/4_JUMP_002.png"), pygame.image.load("images/4_JUMP_003.png"),
                 pygame.image.load("images/4_JUMP_004.png")]

# Character - attack
attack_original = [pygame.image.load("images/5_ATTACK_000.png"), pygame.image.load("images/5_ATTACK_001.png"),
                   pygame.image.load("images/5_ATTACK_002.png"), pygame.image.load("images/5_ATTACK_003.png"),
                   pygame.image.load("images/5_ATTACK_004.png")]

# Character - standing
standing_original = [pygame.image.load("images/standing.png")]

# Platform graphics

platform_images_original = [pygame.image.load("images/platform_1.png"),
                            pygame.image.load("images/platform_2.png")]

# Resize the images

walk_right = []
run_right = []
jump_right = []
attack_right = []
standing_right = []
platform_images = []

def modify_character_size(original_images, resized_images):
    for image in original_images:
        resized_images.append(pygame.transform.scale(image, (int(image.get_width() / 4), int(image.get_height() / 4))))

modify_character_size(walk_original, walk_right)
modify_character_size(run_original, run_right)
modify_character_size(jump_original, jump_right)
modify_character_size(attack_original, attack_right)
modify_character_size(standing_original, standing_right)
modify_character_size(platform_images_original, platform_images)

# Get images for left movements

walk_left = []
run_left = []
jump_left = []
attack_left = []
standing_left = []

def flip_image_horizontally(right_images, left_images):
    for image in right_images:
        left_images.append(pygame.transform.flip(image, True, False))

flip_image_horizontally(walk_right, walk_left)
flip_image_horizontally(walk_right, run_left)
flip_image_horizontally(jump_right, jump_left)
flip_image_horizontally(attack_right, attack_left)
flip_image_horizontally(standing_right, standing_left)
