import pygame
from settings import *
class CoinAnimation(pygame.sprite.Sprite): 
    ANIMATION_DELAY = 6
    def __init__(self, game, x, y):
        self._layer = EFFECTS_LAYER
        pygame.sprite.Sprite.__init__(self, game.all_sprites)
        self.coin_1 = pygame.image.load(coin_1_path).convert_alpha()
        self.coin_1 = pygame.transform.scale2x(self.coin_1)
        self.coin_2 = pygame.image.load(coin_2_path).convert_alpha()
        self.coin_2 = pygame.transform.scale2x(self.coin_2)
        self.coin_3 = pygame.image.load(coin_3_path).convert_alpha()
        self.coin_3 = pygame.transform.scale2x(self.coin_3)
        self.coin_4 = pygame.image.load(coin_4_path).convert_alpha()
        self.coin_4 = pygame.transform.scale2x(self.coin_4)
        self.sprites = [self.coin_1,self.coin_2,self.coin_3,self.coin_4]
        self.sprite_count = 0
        self.image = self.sprites[self.sprite_count]
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.x = x+(BLOCK_SIZE-self.image.get_width())/2
        self.rect.y = y
        self.animation_count = 0
        self.vel_y = -3
        self.time = 30
    def update(self):
        self.rect.y += self.vel_y
        self.animation_count += 1
        self.sprite_count = (self.animation_count // self.ANIMATION_DELAY) % len(self.sprites)
        self.image = self.sprites[self.sprite_count]
        if self.animation_count % self.time == 0:
            self.vel_y*=-1
        if self.animation_count % (self.time*2)==0:
            self.kill()
        
class PlayerDeathAnimation(pygame.sprite.Sprite):
    ANIMATION_DELAY = 1
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        pygame.sprite.Sprite.__init__(self, game.all_sprites)
        self.mario_dead = pygame.image.load(mario_dead_path).convert_alpha()
        self.mario_dead = pygame.transform.scale2x(self.mario_dead)
        self.image = self.mario_dead
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_count = 0
        self.vel_y =3
    def update(self):
        if self.animation_count % self.ANIMATION_DELAY == 0:
            self.rect.y += self.vel_y
            
        if self.rect.top > HEIGHT + BLOCK_SIZE*30:
            self.kill()
            self.game.new()
        self.animation_count += 1
        
class PlayerWinAnimation(pygame.sprite.Sprite):
    ANIMATION_DELAY = 1
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        pygame.sprite.Sprite.__init__(self, game.all_sprites)
        self.mario_win = pygame.image.load(mario_win_path).convert_alpha()
        self.mario_win = pygame.transform.scale2x(self.mario_win)
        self.image = self.mario_win
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_count = 0
        self.vel_y =2
    def update(self):
        if self.animation_count % self.ANIMATION_DELAY == 0:
            self.rect.y += self.vel_y
            
        if self.rect.bottom > HEIGHT - BLOCK_SIZE*3:
            self.vel_y = 0
        self.animation_count += 1
        if self.animation_count >= 300:
            self.kill()
            self.game.new()