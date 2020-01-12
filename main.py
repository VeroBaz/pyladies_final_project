# Platform game - "Jumping Wizard"

import pygame
from settings import *
from sprites import *

class Game():
    def __init__(self):
        # Initialize game window
        pygame.init()
        pygame.mixer.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def new_game(self):
        # Start a new game
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        groundfloor = Groundfloor()
        self.all_sprites.add(groundfloor)
        self.platforms.add(groundfloor)
        for coordinate in PLATFORM_LIST:
            # Explode the list
            platform = Platform(self, *coordinate)
            self.all_sprites.add(platform)
            self.platforms.add(platform)
        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            # Keep loop running at the right speed
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Game loop - events
        for event in pygame.event.get():
            # Check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def update(self):
        # Game loop - update
        self.all_sprites.update()
        # Do not allow jump through platforms
        if self.player.velocity.y < 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.velocity.y = 0
        # Check for collision only if falling - False at the end tells not to delete the sprite
        if self.player.velocity.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest_platform = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest_platform.rect.bottom:
                        lowest_platform = hit
                # Land only if the feet of the character are higher than the platform
                if self.player.position.y < lowest_platform.rect.centery:
                    self.player.position.y = lowest_platform.rect.top
                    self.player.velocity.y = 0

    def draw(self):
        # Game loop - draw
        self.window.blit(BACKGROUND, (0, 0))
        self.all_sprites.draw(self.window)
        # Flip the display - after(!) drawing everything
        pygame.display.flip()

    def show_start_screen(self):
        # Game start screen
        pass

    def show_game_over_screen(self):
        # Game over screen
        pass

game = Game()
game.show_start_screen()
while game.running:
    game.new_game()
    game.show_game_over_screen()

pygame.quit()