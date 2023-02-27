import pygame
from settings import *

class BackgroundSprite(pygame.sprite.Sprite):
    def __init__(self, game, x,y, name=None):
        self._layer = BACKGROUND_LAYER
        self.groups = [game.background_sprites, game.all_sprites]
        pygame.sprite.Sprite.__init__(self, self.groups)
        match name:
            case "cloud1":
                self.image = pygame.image.load(cloud1_path).convert_alpha()
            case "cloud2":
                self.image = pygame.image.load(cloud2_path).convert_alpha()
            case "cloud3":
                self.image = pygame.image.load(cloud3_path).convert_alpha()
            case "shrub1":
                self.image = pygame.image.load(shrub1_path).convert_alpha()
            case "shrub2":
                self.image = pygame.image.load(shrub2_path).convert_alpha()
            case "shrub3":
                self.image = pygame.image.load(shrub3_path).convert_alpha()
            case "hill1":
                self.image = pygame.image.load(hill1_path).convert_alpha()
            case "hill2":
                self.image = pygame.image.load(hill2_path).convert_alpha()
            case "castle":
                self.image = pygame.image.load(castle_path).convert_alpha()
                
            case _:
                print("Error")
                
        self.image = pygame.transform.scale2x(self.image)
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        if name == "shrub1" or name=="shrub2":
            self.rect.x+=BLOCK_SIZE/2     
        if name=="castle":
            self.rect.y -= self.image.get_height()-BLOCK_SIZE

class GravitySprite(pygame.sprite.Sprite): #virtual class DON'T INSTANTIATE
    #REQUIREMENTS FOR VIRTUAL CLASS:
    #Must have function landed(), hit_head()
    #Should set variables self.image, self.rect
    #Must have update() function that calls self.gravity() at top and self.handle_vertical_collision at bottom of function

    GRAVITY = 10
    def __init__(self, game, groups,  layer=ENEMY_LAYER):
        self._layer = layer
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.fall_count = 0 
        self.x_vel = 0
        self.y_vel = 0

        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
    def move(self, dx,dy):
        pass
    
    def gravity(self):
        pass

    def handle_vertical_collision(self, objects):
        collided_objects = []
        hit_head_objects = []
        for obj in objects:
            if pygame.Rect.colliderect(self.rect, obj.rect):
                
                if self.vel.y > 0:
                    self.vel.y = 0
                    self.acc.y = 0
                    self.rect.bottom = obj.rect.top
                    self.landed() #virtual function
                    
                elif self.vel.y < 0:
                    self.vel.y = 0
                    self.acc.y = 0
                    self.rect.top = obj.rect.bottom+1
                    #self.hit_head() #virtual function
                    hit_head_objects.append(self)

                collided_objects.append(obj)
                if self.acc.y > 0:
                    self.acc.y = 0
        return collided_objects, hit_head_objects
        
class Object(pygame.sprite.Sprite):
    def __init__(self, game, x, y, groups, img_path, name=None, layer=PLATFORM_LAYER):
        self._layer = PLATFORM_LAYER
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.name = name    
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.game = game
        