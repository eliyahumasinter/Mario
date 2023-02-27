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
            case _:
                print("Error")
                
        self.image = pygame.transform.scale2x(self.image)
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        if name == "shrub1" or name=="shrub2":
            self.rect.x+=BLOCK_SIZE/2     

class GravitySprite(pygame.sprite.Sprite): #virtual class DON'T INSTANTIATE
    #REQUIREMENTS FOR VIRTUAL CLASS:
    #Must have function landed(), hit_head()
    #Should set variables self.image, self.rect
    #Must have update() function that calls self.gravity() at top and self.handle_vertical_collision at bottom of function

    GRAVITY = 1
    def __init__(self, game, groups,  layer=ENEMY_LAYER):
        self._layer = layer
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.fall_count = 0 
        self.x_vel = 0
        self.y_vel = 0
    def move(self, dx,dy):
        self.rect.x += dx
        self.rect.y += dy
    def gravity(self):
        self.y_vel += min(1, (self.fall_count / 60) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
    def handle_vertical_collision(self, objects, dy):
        collided_objects = []
        for obj in objects:
            if pygame.Rect.colliderect(self.rect, obj.rect):
                if dy > 0:
                    self.rect.bottom = obj.rect.top
                    self.landed() #virtual function
                    
                elif dy < 0:
                    self.rect.top = obj.rect.bottom
                    self.hit_head() #virtual function

                collided_objects.append(obj)
        
        

    


class Goomba(pygame.sprite.Sprite):
    VEL = 1
    ANIMATION_DELAY = 10
    def __init__(self, game, x, y, layer=ENEMY_LAYER):
        self._layer = ENEMY_LAYER
        self.groups = game.all_sprites, game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
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
        self.x_vel = self.VEL
        self.y_vel = 0
        self.squished = False
        
    def update(self):
        if not self.squished:
            if self.x_vel > 0:
                collide_right = self.collide(self.game.walls, self.VEL + 1)
                if collide_right:
                    self.x_vel *= -1
            else:
                collide_left = self.collide(self.game.walls, -(self.VEL + 1))
                if collide_left:
                    self.x_vel *= -1
            self.game.enemies.remove(self)
            collide_with_enemy = pygame.sprite.spritecollide(self, self.game.enemies, False)
            self.game.enemies.add(self)
            if collide_with_enemy:
                self.x_vel*=-1
            self.rect.x+=self.x_vel
        
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
            
        #if jumped on
        # if pygame.Rect.colliderect(self.rect, self.game.player.rect) and self.game.player.y_vel > 0:
        #     self.image = self.image_squished
    def die(self):
        self.image = self.image_squished
        self.x_vel = 0
        if self.squished == False:
            self.rect.y += 16
        self.game.enemies.remove(self)
        self.squished = True
        print("die func")
        

    def move(self, dx,dy):
        self.rect.x += dx
        self.rect.y += dy
        
    def collide(self, objects, dx):
        self.move(dx, 0)
        #self.update_mask()
        collided_object = None
        for obj in objects:
            if pygame.Rect.colliderect(self.rect, obj.rect):
                collided_object = obj
                break
        self.move(-dx, 0)
        #self.update_mask()
        return collided_object
        
        
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
    def __init__(self, game, x, y, name="Platform"):
        groups = [game.all_sprites, game.walls]
        super().__init__(game, x, y, groups, brick_path, name)
        self.hit = False

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
    def update(self):
        self.rect.y+=3
        if self.gotten == False:
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(self.sprites)
            self.image = self.sprites[sprite_index]
            if self.animation_count >= self.ANIMATION_DELAY * len(self.sprites)*5:
                self.animation_count = 0
            self.animation_count += 1
            if self.rect.colliderect(self.game.player.rect) and (self.game.player.jumped == True):
                self.game.coin_count += 1
                self.gotten = True
                self.image = self.gotten_image
            
 
        self.rect.y-=3
        

        