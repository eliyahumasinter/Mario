import pygame
import sys
from os import path
from player import Player
from settings import *
from blockSprites import Ground, Brick, MysteryBox, PipeTop, PipeMiddle, Stair, Flag
from enemySprites import Goomba
from abstractSprites import BackgroundSprite

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.level = 1
        pygame.key.set_repeat(500, 100)
        self.font_name = 'assets\\fonts\\emulogic.ttf'
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, f"assets\\levels\\{LEVELS[1]}"), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        self.coin_audio = pygame.mixer.Sound(coin_audio)
        self.bump_audio = pygame.mixer.Sound(bump_audio)
        self.bump_audio.set_volume(0.3)
        self.jump_audio = pygame.mixer.Sound(jump_audio)
        self.kick_audio = pygame.mixer.Sound(kick_audio)
        self.gameover_audio = pygame.mixer.Sound(gameover_audio)
        
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
        
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.coin_count = 0 
        self.score = 0
        self.playerWon = False
        self.scroll_area_width = WIDTH/2
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.mystery_boxes = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = Player(self)
        self.pole = None
        self.game_over = False
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                match tile:
                    case 'f': #ground brick
                        Ground(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="ground")
                    case 'b': #platform brick
                        Brick(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="brick")
                    case '?': #mystery box
                        MysteryBox(self, col*BLOCK_SIZE, row*BLOCK_SIZE)
                    case '1': #cloud1
                        BackgroundSprite(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="cloud1")
                    case '2': #cloud2
                        BackgroundSprite(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="cloud2")
                    case '3': #cloud3
                        BackgroundSprite(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="cloud3")
                    case '4': #shrub1
                        BackgroundSprite(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="shrub1")
                    case '5': #shrub2
                        BackgroundSprite(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="shrub2")
                    case '6': #shrub3 
                        BackgroundSprite(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="shrub3")
                    case '7': #hill1
                        BackgroundSprite(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="hill1")
                    case '8': #hill2
                        BackgroundSprite(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="hill2")
                    case 'c': #Small castle
                        BackgroundSprite(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="castle")
                    case 't': #top of pipe
                        PipeTop(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="pipe_top")
                    case 'm': #middle of pipe
                        PipeMiddle(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="pipe_middle")
                    case 's': #stair block
                        Stair(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="stair_block")
                    case 'p': #Flag/pole
                        self.pole = Flag(self, col*BLOCK_SIZE, row*BLOCK_SIZE, name="pole")
                        
                    case 'g': #goomba
                        Goomba(self, col*BLOCK_SIZE, row*BLOCK_SIZE)
        
        pygame.mixer.music.load(bg_music)
        pygame.mixer.music.play(loops=-1)
                    

    def run(self):
        # game loop - set self.playing = False to end the game

        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        #self.all_sprites.update()
        if ((self.player.rect.right >= WIDTH - self.scroll_area_width) and self.player.vel.x > 0):
            for sprite in self.all_sprites:
                sprite.rect.x -= self.player.vel.x
                
                

        if (self.player.rect.top >= HEIGHT + BLOCK_SIZE):
            self.game_over = True
            self.player.die()
        
        
        if self.player.rect.x >= self.pole.rect.left+45 and not self.playerWon:
            self.player.win()
        
        self.all_sprites.update()
        
    

    def draw(self):
        fontSize = 20
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen) 
        self.draw_text("SCORE", fontSize, WHITE, BLOCK_SIZE*2, 2)   
        self.draw_text(str(self.score), fontSize, WHITE, BLOCK_SIZE*2, 30)
        self.draw_text("COINS", fontSize, WHITE, BLOCK_SIZE*7, 2)   
        self.draw_text(str(self.coin_count), fontSize, WHITE, BLOCK_SIZE*7+3, 30)
        
        pygame.display.flip()

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if (event.key == pygame.K_SPACE or  event.key == pygame.K_UP) and self.player.jumped == False:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player.moving = False
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.player.jump_cut()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()