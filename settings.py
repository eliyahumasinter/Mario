from pathlib import Path
import os
import pygame.math
BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = os.path.join(BASE_DIR, "assets/images")
SND_DIR  = os.path.join(BASE_DIR, "assets/audio")

BLOCK_SIZE = 32
WIDTH = 32*BLOCK_SIZE  #32 blocks
HEIGHT = 15*BLOCK_SIZE #15 blocks
FPS = 60
TITLE = "Mario"
BG_COLOR = (92,148,252)
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
MB_COLOR  = (200,200,0)

LEVELS = {
    1: "level1.txt"
}
GRAVITY_ACC_CONST = 0.5
PLAYER_ACC = GRAVITY_ACC_CONST
PLAYER_FRICTION = -0.07
MAX_PLAYER_VEL = 4
ENEMY_FRICTION  = -0.15
PLAYER_JUMP_HEIGHT = 12

#Layers
PLAYER_LAYER = 5
ENEMY_LAYER = 4
PLATFORM_LAYER = 3
EFFECTS_LAYER = 2
BACKGROUND_LAYER = 1
FONT_NAME = "arial"


#Image Paths

brick_path = os.path.join(IMG_DIR, "brick_block.png")
stair_block_path = os.path.join(IMG_DIR, "stair_block.png")
floor_path = os.path.join(IMG_DIR, 'floor.png')
cloud1_path = os.path.join(IMG_DIR, 'cloud1.png')
cloud2_path = os.path.join(IMG_DIR, 'cloud2.png')
cloud3_path = os.path.join(IMG_DIR, 'cloud3.png')
shrub1_path = os.path.join(IMG_DIR, 'shrub1.png')
shrub2_path = os.path.join(IMG_DIR, 'shrub2.png')
shrub3_path = os.path.join(IMG_DIR, 'shrub3.png')
hill1_path = os.path.join(IMG_DIR, 'hill1.png')
hill2_path = os.path.join(IMG_DIR, 'hill2.png')
pipe_top_path = os.path.join(IMG_DIR, 'pipe_top.png')
pipe_middle_path = os.path.join(IMG_DIR, 'pipe_middle.png')


#Coins
coin_1_path = os.path.join(IMG_DIR, 'coin1.png')
coin_2_path = os.path.join(IMG_DIR, 'coin2.png')
coin_3_path = os.path.join(IMG_DIR, 'coin3.png')
coin_4_path = os.path.join(IMG_DIR, 'coin4.png')

#Mario
mario_idle_path = os.path.join(IMG_DIR, 'mario_idle.png')
mario_walk_1_path = os.path.join(IMG_DIR, 'mario_walk_1.png')
mario_walk_2_path = os.path.join(IMG_DIR, 'mario_walk_2.png')
mario_walk_3_path = os.path.join(IMG_DIR, 'mario_walk_3.png')
mario_jump_path = os.path.join(IMG_DIR, 'mario_jump.png')
mario_turn_around_path = os.path.join(IMG_DIR, 'mario_turn_around.png')
mario_dead_path = os.path.join(IMG_DIR, 'mario_dead.png')
mario_win_path = os.path.join(IMG_DIR, 'mario_win.png')

#Mystery Box
question_mark_block_path = os.path.join(IMG_DIR, 'question_mark_block.png')
question_mark_block_2_path = os.path.join(IMG_DIR, 'question_mark_block_2.png')
question_mark_block_3_path = os.path.join(IMG_DIR, 'question_mark_block_3.png')
question_mark_block_gotten_path = os.path.join(IMG_DIR, 'question_mark_block_gotten.png')

#Goombas
goomba_1_path = os.path.join(IMG_DIR, 'enemy1.png')
goomba_2_path = os.path.join(IMG_DIR, 'enemy2.png')
goomba_squished_path = os.path.join(IMG_DIR, 'enemy_squished.png')

castle_path = os.path.join(IMG_DIR, 'castle.png')
flag_path = os.path.join(IMG_DIR, "flag.png")


vec = pygame.math.Vector2


#Music/audio
bg_music = os.path.join(SND_DIR, 'bg_music.mp3')
coin_audio = os.path.join(SND_DIR, 'coin.wav')
jump_audio = os.path.join(SND_DIR, 'jump_small.wav')
bump_audio = os.path.join(SND_DIR, 'bump.wav')
kick_audio = os.path.join(SND_DIR, 'kick.wav')
gameover_audio = os.path.join(SND_DIR, 'gameover.wav')
