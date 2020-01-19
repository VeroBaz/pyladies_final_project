# Platform game - "Jumping Wizard"

import pygame
from settings import *
from sprites import *
from os import path


class Game:
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
        # Load high score
        self.directory = path.dirname(__file__)
        with open(path.join(self.directory, HIGH_SCORE_FILE), "r") as file:
            try:
                self.high_score = int(file.read())
            except:
                self.high_score = 0
        # Load sounds - have to be saved in the directory called "sounds"
        self.sounds_directory = path.join(self.directory, "sounds")
        self.coin_sound = pygame.mixer.Sound(path.join(self.sounds_directory, "collect_coin.wav"))
        self.monster_sound = pygame.mixer.Sound(path.join(self.sounds_directory, "life_lost.wav"))
        self.game_over_sound = pygame.mixer.Sound(path.join(self.sounds_directory, "game_over.wav"))

    def new_game(self):
        # Start a new game
        self.score = 0
        # Create groups for the sprites
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        # Create ground floor
        ground_floor = GroundFloor()
        self.all_sprites.add(ground_floor)
        self.platforms.add(ground_floor)
        # Create platforms
        for coordinate in PLATFORM_LIST:
            # Explode the list
            platform = Platform(self, *coordinate)
            self.all_sprites.add(platform)
            self.platforms.add(platform)
        # Create coin
        self.coin = Coin()
        self.all_sprites.add(self.coin)
        self.coins.add(self.coin)
        # Create player character
        self.player = Player(self)
        self.all_sprites.add(self.player)
        # Create monster
        self.monster = Monster()
        self.all_sprites.add(self.monster)
        self.monsters.add(self.monster)
        # Check whether monster was created at the same spot as player is
        while self.monster_character_same_spot(self.player, self.monsters):
            self.monster.kill()
            self.monster = Monster()
            self.all_sprites.add(self.monster)
            self.monsters.add(self.monster)
        self.all_sprites.add(self.monster)
        self.monsters.add(self.monster)
        pygame.mixer.music.load(path.join(self.sounds_directory, "background_music.ogg"))
        # Credits for background music: "Mushroom Dance" by bart
        # licensed CC-BY 3.0, CC-BY-SA 3.0, GPL 3.0, or GPL 2.0:
        # https://opengameart.org/content/mushroom-dance
        self.run()

    def monster_character_same_spot(self, player, monsters):
        if pygame.sprite.spritecollide(player, monsters, False):
            return True
        else:
            return False

    def run(self):
        # Game loop
        pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            # Keep loop running at the right speed
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)

    def events(self):
        # Game loop - events
        for event in pygame.event.get():
            # Check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # Check for jump
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
                # lowest_platform = hits[0]
                # for hit in hits:
                #     if hit.rect.bottom > lowest_platform.rect.bottom:
                #         lowest_platform = hit
                # Land only if the feet of the character are higher than the platform
                if self.player.rect.bottom < hits[0].rect.centery:
                    self.player.position.y = hits[0].rect.top
                    self.player.velocity.y = 0

        # Check for collision between character and coin
        hits_coin = pygame.sprite.spritecollide(self.player, self.coins, True)
        if hits_coin:
            self.score += 10
            self.coin_sound.play()
            self.coin = Coin( )
            self.all_sprites.add(self.coin)
            self.coins.add(self.coin)

        # Check for collision between center of the character and monster
        if self.monster.rect.collidepoint(self.player.rect.center):
            self.monster.kill()
            self.player.lives -= 1
            if self.player.lives >= 1:
                self.monster_sound.play()
            self.monster = Monster()
            self.all_sprites.add(self.monster)
            self.monsters.add(self.monster)
            # Check whether monster was created at the same spot as player is
            while self.monster_character_same_spot(self.player, self.monsters):
                self.monster.kill()
                self.monster = Monster()
                self.all_sprites.add(self.monster)
                self.monsters.add(self.monster)

        # Check whether coins and monsters are at the same position - force monster to move again
        hits_coins_monsters = pygame.sprite.spritecollide(self.coin, self.monsters, True)
        if hits_coins_monsters:
            self.monster = Monster()
            self.all_sprites.add(self.monster)
            self.monsters.add(self.monster)

        # No lives left - end of the game
        if self.player.lives <= 0:
            self.playing = False

    def draw(self):
        # Game loop - draw
        self.window.blit(BACKGROUND, (0, 0))
        self.all_sprites.draw(self.window)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH - 60, 15)
        self.draw_text("Lives: " + str(self.player.lives), 22, WHITE, WIDTH - 60, 40)
        # Flip the display - after(!) drawing everything
        pygame.display.flip()

    def show_start_screen(self):
        # Game start screen
        pygame.mixer.music.load(path.join(self.sounds_directory, "opening_music.ogg"))
        pygame.mixer.music.play(loops=-1)
        self.window.blit(BACKGROUND, (0, 0))
        self.draw_text(TITLE, 58, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Collect the coins, beware of monsters", 22, WHITE, WIDTH / 2, (HEIGHT / 2) - 20)
        self.draw_text("Use arrows to move the wizard", 22, WHITE, WIDTH / 2, (HEIGHT / 2) + 10)
        self.draw_text("Space to jump", 22, WHITE, WIDTH / 2, (HEIGHT / 2) + 40)
        self.draw_text("Press Enter to play", 22, WHITE, WIDTH / 2, (HEIGHT * 3) / 4)
        self.draw_text("High Score: " + str(self.high_score), 22, WHITE, WIDTH / 2, 15)
        pygame.display.flip()
        self.wait_for_key()

    def show_game_over_screen(self):
        # Game over screen
        if not self.running:
            return
        self.game_over_sound.play()
        self.window.blit(BACKGROUND, (0, 0))
        self.draw_text("GAME OVER", 78, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Your score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press Enter to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.high_score:
            self.high_score = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 50)
            with open(path.join(self.directory, HIGH_SCORE_FILE), "w") as file:
                file.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.high_score), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 50)
        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)

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
                    if event.key == pygame.K_RETURN:
                        waiting = False


game = Game()
game.show_start_screen()
while game.running:
    game.new_game()
    game.show_game_over_screen()

pygame.quit()
