import pygame

pygame.font.init()

score = 0
enemy_y = 265
enemy_x = 700
speed = 0
player_x = 20
player_y = 215
player_y_velocity = 0
player_gravity = 0
screen = pygame.display.set_mode((800,400))

game_active = True

clock = pygame.time.Clock()

font = pygame.font.Font('font/Pixeltype.ttf',50)
button_font = pygame.font.Font('font/Roboto-Black.ttf',30)
game_over_font = pygame.font.Font('font/gameover.ttf',50)
quit_text_x = 70
quit_text_y = 10
try_again_text_x = 35
try_again_text_y = 10
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_two_surface = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
tree_1_surface = pygame.image.load('graphics/Tree/tree1.png').convert_alpha()
tree_2_surface = pygame.image.load('graphics/Tree/tree2.png').convert_alpha()
tree_1_rect = tree_1_surface.get_rect()
tree_2_rect = tree_2_surface.get_rect()
tree_1_rect.x = 2000
tree_2_rect.x = 2500
ground_rect = ground_surface.get_rect()
sky_rect = sky_surface.get_rect()
snail_rect = snail_surface.get_rect(bottomright = (800,300))
player_rect = player_surface.get_rect(topleft = (player_x,player_y))
passed_snail = False