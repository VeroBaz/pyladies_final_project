# Sprites for the game

import pygame
from random import choice
from settings import *
from graphics import *
vector = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.attack = False
        # Keep track which image is displayed
        self.current_image = 0
        # Keep track of time how long the image is displayed
        self.last_update = 0
        self.image = standing_right[0]
        self.rect = self.image.get_rect()
        # Shrink rectangle so the collisions are less sensitive
        self.rect.inflate_ip(-8.6, -7.7)
        self.position = vector(WIDTH / 10, HEIGHT - HEIGHT / 4)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.lives = 3

    def jump(self):
        # Jump only if standing on platform
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.velocity.y = -PLAYER_JUMP

    def update(self):
        self.animate()
        self.acceleration = vector(0, PLAYER_GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.acceleration.x = -PLAYER_ACCELERATION
        if keys[pygame.K_RIGHT] and self.rect.x + self.image.get_size()[0] < WIDTH:
            self.acceleration.x = PLAYER_ACCELERATION

        # Apply friction
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION
        # Calculate the motions
        self.velocity += self.acceleration
        if abs(self.velocity.x) < 0.3:
            self.velocity.x = 0
        self.position += self.velocity + 0.5 * self.acceleration
        self.rect.midbottom = self.position

        # Keep player within the window
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def animate(self):
        current_time = pygame.time.get_ticks()
        # Get info - character walking
        if self.velocity.x != 0 and self.velocity.y == 0:
            self.walking = True
        else:
            self.walking = False
        # Show walking animation
        if self.walking:
            if current_time - self.last_update > 100:
                self.last_update = current_time
                self.current_image = (self.current_image + 1) % len(walk_right)
                if self.velocity.x > 0:
                    self.image = walk_right[self.current_image]
                else:
                    self.image = walk_left[self.current_image]
        # Get info - character jumping
        if self.velocity.y != 0:
            self.jumping = True
        else:
            self.jumping = False
        # Show jumping animation
        if self.jumping:
            if current_time - self.last_update > 100:
                self.last_update = current_time
                self.current_image = (self.current_image + 1) % len(jump_right)
                if self.velocity.x == 0 or self.velocity.x > 0:
                    self.image = jump_right[self.current_image]
                else:
                    self.image = jump_left[self.current_image]


class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image=platform_images[0]):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class GroundFloor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, HEIGHT - 20))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - 30


class InteractiveSprites(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.game = game
        self.last_update = 0
        self.rect = self.image.get_rect()
        self.position = choice(coins_monsters_positions)
        self.last_position = self.position
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def change_position(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.time:
            self.last_update = current_time
            # Prevent sprite to appear at the same spot
            while self.position == self.last_position:
                self.position = choice(coins_monsters_positions)
                # Get x and y for monsters (different size than coins)
                try:
                    self.rect.x = self.position[0] - self.monster_position_x
                    self.rect.y = self.position[1] - self.monster_position_y
                # Get x and y for coins
                except AttributeError:
                    self.rect.x = self.position[0]
                    self.rect.y = self.position[1]
            self.last_position = self.position
            # Get info whether monster is moving to change image (does not apply to coins)
            try:
                self.moving = True
            except AttributeError:
                pass

    def update(self):
        self.change_position()
        # Change monster image (does not apply to coins)
        try:
            self.change_image()
            self.moving = False
        except AttributeError:
            pass


class Coin(InteractiveSprites):
    def __init__(self):
        self.image = coin_image[0]
        self.time = 8000
        super().__init__()
        # Shrink rectangle so the collisions are less sensitive
        self.rect.inflate_ip(-3.5, -3.5)


class Monster(InteractiveSprites):
    def __init__(self):
        self.image = choice(monsters_images)
        self.last_image = self.image
        self.time = 5000
        self.moving = False
        super().__init__()
        self.monster_position_x = 20
        self.monster_position_y = 15
        self.rect.x = self.rect.x - self.monster_position_x
        self.rect.y = self.rect.y - self.monster_position_y

    def change_image(self):
        if self.moving:
            while self.image == self.last_image:
                self.image = choice(monsters_images)
            self.last_image = self.image
