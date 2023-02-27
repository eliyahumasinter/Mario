import pygame
from settings import *
from abstractSprites import GravitySprite

class Goomba(GravitySprite):
    VEL = 1
    ANIMATION_DELAY = 10
    def __init__(self, game, x, y):
        super().__init__(game, [game.all_sprites, game.enemies]) #Layer is default to enemy
       
        self.image1 = pygame.image.load(goomba_1_path).convert_alpha()
        self.image1 = pygame.transform.scale2x(self.image1)
        self.image2 = pygame.image.load(goomba_2_path).convert_alpha()
        self.image2 = pygame.transform.scale2x(self.image2)
        self.image_squished = pygame.image.load(goomba_squished_path).convert_alpha()
        self.image_squished = pygame.transform.scale2x(self.image_squished)
        self.sprites = [self.image1, self.image2]
        
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.animation_count = 0
        self.die_count = 0
        self.squished = False
        self.in_air = False
        self.vel = vec(-self.VEL,0)
        self.y_vel=0
        self.acc = vec(0,0)
        
        
    def update(self):
        #animation
        if not self.squished:
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(self.sprites)
            self.image = self.sprites[sprite_index]
            if self.animation_count >= self.ANIMATION_DELAY * len(self.sprites)*5:
                self.animation_count = 0
            self.animation_count += 1
        else:
            if self.die_count >= self.ANIMATION_DELAY * 3:
                self.kill()
            self.die_count += 1
            
        
        if round(self.vel.y) > 0:
            self.in_air = True
        
        if self.rect.top >= HEIGHT+BLOCK_SIZE:
            self.kill()
        
        if not self.squished:
            if not self.in_air:
                if self.vel.x > 0:
                    collide_right = self.collide(self.game.walls, 3)
                    if collide_right:
                        self.vel.x *= -1
                       
                else:
                    collide_left = self.collide(self.game.walls, -3)
                    if collide_left:
                        self.vel.x *= -1
                        
                self.game.enemies.remove(self)
                collide_with_enemy = pygame.sprite.spritecollide(self, self.game.enemies, False)
                self.game.enemies.add(self)
                if collide_with_enemy:
                    self.vel.x*=-1
                    
                   
                
                if (self.rect.x - self.game.player.rect.x) <= WIDTH+BLOCK_SIZE*2: #start moving once four only two blocks until visible
                    self.rect.x+=self.vel.x
        
        #gravity
        self.acc.y = GRAVITY_ACC_CONST
        self.vel.y += self.acc.y #
        self.rect.y += self.vel.y + 0.5*self.acc.y
        
 

        self.handle_vertical_collision(self.game.walls)
        
    def die(self):
        self.image = self.image_squished
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.vel.x = 0
        if self.squished == False:
            self.rect.y += 16
        self.game.enemies.remove(self)
        self.squished = True
        print("die func")
        

        
    def collide(self, objects, dx):
        self.rect.x += dx
        collided_object = None
        for obj in objects:
            if pygame.Rect.colliderect(self.rect, obj.rect):
                collided_object = obj
                break
        self.rect.x -= dx
        return collided_object
 
    
    def landed(self):
        self.fall_count = 0
        self.vel.y = 0 
        self.in_air = False
        
    def hit_head(self): #unlikely to trigger
        self.fall_count = 0
        self.vel.y += 1
      