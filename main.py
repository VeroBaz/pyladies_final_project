# Platform game - "Jumping Wizard"

import pygame
from settings import *
from sprites import *
from os import path

class Game():
    def __init__(self):
        # Initialize game window
        pygame.init()
        pygame.mixer.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # Load highscore
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HIGHSCORE_FILE), "w") as file:
            try:
                self.highscore = int(file.read())
            except:
                self.highscore = 0

    def new_game(self):
        # Start a new game
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
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
        self.coin = Coin(self)
        # self.all_sprites.add(self.coin)
        self.coins.add(self.coin)
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
        self.coins.update()
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
        # Check for collision between character and coin
        hits_coin = pygame.sprite.spritecollide(self.player, self.coins, True)
        if hits_coin:
            self.score += 10
            self.coin = Coin(self)
            # self.all_sprites.add(self.coin)
            self.coins.add(self.coin)

        # Die
        if self.player.health <= 0:
            self.playing = False

    def draw(self):
        # Game loop - draw
        self.window.blit(BACKGROUND, (0, 0))
        self.all_sprites.draw(self.window)
        self.coins.draw(self.window)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH - 50, 15)
        # Flip the display - after(!) drawing everything
        pygame.display.flip()

    def show_start_screen(self):
        # Game start screen
        self.window.fill(VIOLET)
        self.draw_text(TITLE, 46, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Use arrows to move the wizard", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Space to jump", 22, WHITE, WIDTH / 2, (HEIGHT / 2) + 30)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, (HEIGHT * 3) / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pygame.display.flip()
        self.wait_for_key()

    def show_game_over_screen(self):
        # Game over screen
        if not self.running:
            return
        self.window.fill(VIOLET)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEGHT / 2 + 50)
            with open(path.join(self.dir, HIGHSCORE_FILE), "w") as file:
                file.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEGHT / 2 + 50)
        pygame.display.flip()
        self.wait_for_key()

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.window.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

game = Game()
game.show_start_screen()
while game.running:
    game.new_game()
    game.show_game_over_screen()

pygame.quit()