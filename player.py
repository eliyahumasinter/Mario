import pygame
from settings import *
from abstractSprites import GravitySprite
from animationSprites import PlayerDeathAnimation, PlayerWinAnimation

class Player(GravitySprite):
    COLOR = (40,234,140)
    VEL = 3
    ANIMATION_DELAY = 7
    
    def __init__(self, game):
        super().__init__(game, game.all_sprites, layer = PLAYER_LAYER)

        self.mario_dead = pygame.image.load(mario_dead_path).convert_alpha()
        self.mario_idle = pygame.image.load(mario_idle_path).convert_alpha()
        self.mario_idle = pygame.transform.scale2x(self.mario_idle)
        
        self.mario_walk_1 = pygame.image.load(mario_walk_1_path).convert_alpha()
        self.mario_walk_1 = pygame.transform.scale2x(self.mario_walk_1)
        
        self.mario_walk_2 = pygame.image.load(mario_walk_2_path).convert_alpha()
        self.mario_walk_2 = pygame.transform.scale2x(self.mario_walk_2)
        
        self.mario_walk_3 = pygame.image.load(mario_walk_3_path).convert_alpha()
        self.mario_walk_3 = pygame.transform.scale2x(self.mario_walk_3)
        
        self.mario_jump = pygame.image.load(mario_jump_path).convert_alpha()
        self.mario_jump = pygame.transform.scale2x(self.mario_jump)
        
        self.mario_turn_around = pygame.image.load(mario_turn_around_path).convert_alpha()
        self.mario_turn_around = pygame.transform.scale2x(self.mario_turn_around)
        
        self.mario_idle_left = pygame.transform.flip(self.mario_idle, True, False) 
        self.mario_jump_left = pygame.transform.flip(self.mario_jump, True, False)
        self.mario_walk_1_left = pygame.transform.flip(self.mario_walk_1, True, False)
        self.mario_walk_2_left = pygame.transform.flip(self.mario_walk_2, True, False)
        self.mario_walk_3_left = pygame.transform.flip(self.mario_walk_3, True, False)
        self.mario_turn_around_left = pygame.transform.flip(self.mario_turn_around, True, False)
        
        
        self.image = self.mario_idle
        self.rect = self.image.get_rect()
        self.rect.x = BLOCK_SIZE*3 
        self.rect.y = -BLOCK_SIZE*2
        
        

        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
        
        self.direction = "right"
        self.animation_count = 0
        self.fall_count = 0
        self.jumped = False
        self.moving = False
           
    def jump(self, name=None):
        
        self.fall_count = 0
        if name == None:
            self.game.jump_audio.play()
            self.vel.y = -PLAYER_JUMP_HEIGHT
            self.animation_count = 0
            self.jumped = True
        elif name == "kill_jump":
            self.game.kick_audio.play()
            self.vel.y = -5    
    
    def jump_cut(self):
        if self.jumped:
            if self.vel.y < -3:
                self.vel.y = -3
    
        
    def move_left(self):
        self.moving = True
        self.acc.x = -PLAYER_ACC
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
        

    def move_right(self):
        self.moving = True
        self.acc.x = PLAYER_ACC
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
            
    def update(self):
        self.update_sprite() #check
        self.handle_move(self.game.walls)
        collide_left = self.collide(self.game.enemies, -(self.VEL ))
        collide_right = self.collide(self.game.enemies, self.VEL)
        if (collide_left or collide_right) and (not (self.vel.y > 0.5)):
            enemy = collide_left if collide_left else collide_right
            #enemy.vel.x = 0
            self.die()
           
        for enemy in self.game.enemies:
            if pygame.Rect.colliderect(self.rect, enemy.rect):
                if self.vel.y > 0.5:
                    #Landed on enemy
                    enemy.die()
                    self.game.score += 100
                    self.game.enemies.remove(self)
                    self.jump(name="kill_jump")
                    
                    
                elif self.vel.y < 0:
                    self.die()
        
        self.handle_vertical_collision(self.game.walls) #last
        
    def update_sprite(self):
        if self.jumped:
            if self.direction == "right":
                self.image = self.mario_jump
            else:
                self.image = self.mario_jump_left
        elif self.vel.x > 0.3:
            sprites = [self.mario_walk_2,
                       self.mario_walk_3,
                       self.mario_walk_1]
    
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
            self.image = sprites[sprite_index]
            self.animation_count += 1
        elif self.vel.x < -0.3:
            sprites = [self.mario_walk_2_left,
                       self.mario_walk_3_left,
                       self.mario_walk_1_left]
    
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
            self.image = sprites[sprite_index]
            self.animation_count += 1
        
        
        if round(self.vel.x)==0:
            if self.jumped == False:
                if self.direction == "right":
                    self.image = self.mario_idle
                else:
                    self.image = self.mario_idle_left
                    
        if round(self.vel.x) < 0 and round(self.acc.x)>0:
            self.image = self.mario_turn_around
        if round(self.vel.x) > 0 and round(self.acc.x)<0:
            self.image = self.mario_turn_around_left

    def landed(self):
        self.fall_count = 0
        self.vel.y = 0
        self.jumped = False
        
    def hit_head(self, objects):
        self.fall_count = 0
        self.rect.y += 1
        
       
    def collide(self, objects, dx):
        self.rect.x += dx
        collided_object = None
        for obj in objects:
            if pygame.Rect.colliderect(self.rect, obj.rect):
                collided_object = obj
                break

        self.rect.x -= dx
        
        return collided_object
      
    def handle_move(self, objects):
        keys = pygame.key.get_pressed()

        self.acc = vec(0,0.5)
        collide_left = self.collide(objects, -MAX_PLAYER_VEL-1)
        collide_right = self.collide(objects, MAX_PLAYER_VEL)
        if collide_right or collide_left:
            self.vel.x = 0
            self.acc.x = 0
            
        if keys[pygame.K_LEFT] and not collide_left and self.rect.left > 0:
            self.move_left()
        if keys[pygame.K_RIGHT] and not collide_right:
            self.move_right()
        if self.rect.left < 0:
            self.rect.left = 0
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        
        self.rect.x += min(round(self.vel.x + 0.5*self.acc.x),MAX_PLAYER_VEL)
        self.rect.y += self.vel.y + 0.5*self.acc.y

        _, hit_head_objects = self.handle_vertical_collision(objects)
        if hit_head_objects:
            self.hit_head(hit_head_objects)
    
    def die(self):
        pygame.mixer.music.stop()
        self.vel.x = 0
        self.game.gameover_audio.play()
        self.jump() #jump a little
        self.kill()
        x = self.rect.x
        y = self.rect.y

        PlayerDeathAnimation(self.game, x,y)
    
    def win(self):
        self.vel.x = 0
        self.kill()
        self.game.playerWon = True
        x = self.rect.x
        y = self.rect.y
        PlayerWinAnimation(self.game, x,y)

        