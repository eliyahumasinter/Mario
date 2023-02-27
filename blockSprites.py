import pygame
from settings import *
from abstractSprites import Object
from animationSprites import CoinAnimation


class PipeTop(Object):
    def __init__(self, game, x, y, name="platform"):
        groups = [game.all_sprites, game.walls]
        super().__init__(game, x, y, groups, pipe_top_path, name)
    
class PipeMiddle(Object):
    def __init__(self, game, x, y, name="pipe_top"):
        groups = [game.all_sprites, game.walls]
        super().__init__(game, x, y, groups, pipe_middle_path, name)
        
class Ground(Object):
    def __init__(self, game, x, y, name="pipe_middle"):
        groups = [game.all_sprites, game.walls]
        super().__init__(game, x, y, groups, floor_path, name)

class Brick(Object):
    def __init__(self, game, x, y, name="platform"):
        groups = [game.all_sprites, game.walls]
        super().__init__(game, x, y, groups, brick_path, name)
        self.hit = False
        self.animation_count = 0
        self.time = 16
        self.speed = 1
        self.y = y
    def update(self):
        self.rect.y+=3
        
        if self.rect.colliderect(self.game.player.rect) and (self.game.player.jumped == True):
            self.hit = True

        if self.hit:
            self.game.bump_audio.play()
            if self.animation_count <= self.time/2:
                self.rect.y -= self.speed
            elif self.animation_count > self.time/2:
                self.rect.y += self.speed
                
            if self.animation_count == self.time:
                self.animation_count = 0
                self.hit = False
                self.y_vel = 0 
                self.rect.y = self.y  + 3                 
            self.animation_count += 1
            
        self.rect.y-=3
        

class Stair(Object):
    def __init__(self, game, x, y, name="stair_block"):
        groups = [game.all_sprites, game.walls]
        super().__init__(game, x, y, groups, stair_block_path, name)
        
class Flag(Object):
    def __init__(self, game, x, y, name="flag"):
        groups = [game.all_sprites]
        super().__init__(game, x, y, groups, flag_path, name)
        self.rect.y -= self.image.get_height()-BLOCK_SIZE

        


class MysteryBox(Object):
    ANIMATION_DELAY = 15
    
    def __init__(self, game, x, y, name="Mystery Box"):
        groups = [game.all_sprites, game.walls, game.mystery_boxes]
        super().__init__(game, x, y, groups, question_mark_block_path, name)
        self.gotten = False
        self.gotten_image = pygame.image.load(question_mark_block_gotten_path).convert_alpha()
        self.gotten_image = pygame.transform.scale2x(self.gotten_image)
        
        self.question_mark_block = pygame.image.load(question_mark_block_path).convert_alpha()
        self.question_mark_block = pygame.transform.scale2x(self.question_mark_block)
        
        self.question_mark_block_2 = pygame.image.load(question_mark_block_2_path).convert_alpha()
        self.question_mark_block_2 = pygame.transform.scale2x(self.question_mark_block_2)
        
        self.question_mark_block_3 = pygame.image.load(question_mark_block_3_path).convert_alpha()
        self.question_mark_block_3 = pygame.transform.scale2x(self.question_mark_block_3)
        
        
        self.sprites = [self.question_mark_block,
                        self.question_mark_block_2,
                        self.question_mark_block_3]
        
        self.animation_count = 0
        self.bounce = False
        self.y = y
    def update(self):
        self.rect.y+=3
        if self.gotten == False:
            
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(self.sprites)
            self.image = self.sprites[sprite_index]
            if self.animation_count >= self.ANIMATION_DELAY * len(self.sprites)*5:
                self.animation_count = 0
            self.animation_count += 1
            if self.rect.colliderect(self.game.player.rect) and (self.game.player.jumped == True):
                CoinAnimation(self.game, self.rect.x,self.rect.y)
                self.game.coin_audio.play()
                self.game.coin_count += 1
                self.game.score += 200
                self.gotten = True
                self.bounce = True
                self.speed = 2
                self.image = self.gotten_image
                self.animation_count = 0
        else:
            if self.rect.colliderect(self.game.player.rect) and (self.game.player.jumped == True):
                self.game.bump_audio.play()
                
        if self.bounce:
            if self.animation_count <= 4:
                self.rect.y -= self.speed
            elif self.animation_count > 4:
                self.rect.y += self.speed
                
            if self.animation_count == 8:
                self.bounce = False
                self.animation_count = 0
                self.rect.y = self.y  + 3    
            self.animation_count += 1   

        self.rect.y-=3
        
        

        