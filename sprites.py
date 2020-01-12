# Sprites for the game

import pygame
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
        self.position = vector(WIDTH / 10, HEIGHT - HEIGHT / 4)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

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
        if keys[pygame.K_RIGHT] and self.rect.x + 30 < WIDTH:
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
        self.edges = pygame.Surface((WIDTH, HEIGHT)).get_rect()
        self.rect.clamp_ip(self.edges)

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
                bottom = self.rect.bottom
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
            if current_time - self.last_update > 200:
                self.last_update = current_time
                self.current_image = (self.current_image + 1) % len(jump_right)
                bottom = self.rect.bottom
                if self.velocity.x == 0 or self.velocity.x > 0:
                    self.image = jump_right[self.current_image]
                else:
                    self.image = jump_left[self.current_image]
        # TO DO Get info - character attack
        # TO DO Show attack animation

class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type=platform_images[0]):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = type
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Groundfloor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, HEIGHT - 20))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - 20
