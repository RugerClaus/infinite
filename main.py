import pygame
from magic import tree_magic

pygame.init()
pygame.font.init()

pygame.display.set_caption("PITS: Pie In The Sky")
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()

score = 0
enemy_y = 265
enemy_x = 800
speed = 0
player_x = 20
player_y = 300
player_y_velocity = 0
player_gravity = 0



sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_two_surface = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(topleft = (player_x,player_y))
tree_1_surface = pygame.image.load('graphics/Tree/tree1.png').convert_alpha()
tree_2_surface = pygame.image.load('graphics/Tree/tree2.png').convert_alpha()
tree_1_rect = tree_1_surface.get_rect()
tree_2_rect = tree_2_surface.get_rect()
tree_1_rect.x = 1000
tree_2_rect.x = 1500
ground_rect = ground_surface.get_rect()
sky_rect = sky_surface.get_rect()
snail_rect = snail_surface.get_rect(bottomright = (800,300))
passed_snail = False







game_active = False
running = False

#fonts
font = pygame.font.Font('font/Pixeltype.ttf',50)
button_font = pygame.font.Font('font/Roboto-Black.ttf',30)
game_over_font = pygame.font.Font('font/gameover.ttf',50)

#buttons:

#play button
play_surface = pygame.Surface((200,50))
play_rect = play_surface.get_rect(center = (200,200))

#quit
quit_surface = pygame.Surface((200,50))
quit_text = button_font.render("Quit",True,'white')
quit_rect = play_surface.get_rect(center = (600,200))

#try again
try_again_surface = pygame.Surface((200,50))
try_again_text = button_font.render("Try Again",True,'white')
try_again_rect = try_again_surface.get_rect(center = (200,200))

#text
game_over_text = font.render("Welcome To The Game!",True,(255,255,255))
play_text = font.render("Play",True,'white')
quit_text = font.render("Quit",True,'white')

#text locations
play_text_x = 70
play_text_y = 10
quit_text_x = 70
quit_text_y = 10
try_again_text_x = 35
try_again_text_y = 10
menu = True




def start():
    global game_active,player_x,play_text,quit_text,clock,player_rect,quit_rect,speed,player_gravity



    run = True
    while run:
        if menu == False:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_active = True
                    game()
                if event.key == pygame.K_d and speed <= 0 and game_active == True:
                    speed = 2
                if event.key == pygame.K_a and speed == 2 and game_active == True:
                    speed = -2
                if event.key == pygame.K_SPACE and player_rect.bottom == 300 and game_active == True:
                    player_gravity = -8.5
        clock.tick(60)

        pygame.display.flip()

def game():
    
    global menu,game_active,player_gravity,score,sky_surface,ground_surface,score_surface,tree_1_rect,tree_2_rect,tree_1_surface,tree_2_surface,snail_rect,snail_surface,player_rect,player_surface,player_x,running,speed,clock,screen,speed

    menu = False
    

    while game_active:
        
        running = True


        score_surface = font.render(f'Score: {score}',True,(64,64,64))
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        screen.blit(score_surface,(650,5))

        tree_1_rect.x -= 2
        tree_2_rect.x -= 2
        tree_1_rect.bottom = 300
        tree_2_rect.bottom = 300
        if tree_1_rect.right <= 0: 
            tree_magic(tree_1_rect)
        if tree_2_rect.right <= 0: 
            tree_magic(tree_2_rect)
            screen.blit(tree_1_surface,tree_1_rect)
            screen.blit(tree_2_surface,tree_2_rect)

        snail_rect.x -= 3
        if snail_rect.right <= 0: 
            snail_rect.left = 800
            screen.blit(snail_surface,snail_rect)

        player_gravity += 0.2
        player_rect.bottom += player_gravity
        screen.blit(player_surface,player_rect)

        player_x += speed
        player_rect.x = player_x
        if player_rect.bottom > 299: 
            player_rect.bottom = 300
            player_gravity = 0
        if player_rect.left < 0:
            player_rect.left = 0
            speed = 2
            player_gravity = -8.5
        if player_rect.right > 800:
            player_rect.right = 800
            speed = -2
            player_gravity = -8.5
        if snail_rect.colliderect(player_rect):
            game_active = False


        if player_rect.right > snail_rect.left and not passed_snail:
            passed_snail = True
            score += 1
        if snail_rect.left > player_rect.right:
            passed_snail = False
        game_active = True
    clock.tick(60)
    pygame.display.flip()

def game_over():
    global score,speed,game_active,game_over_font,quit_text_x,quit_text_y,try_again_text_x,try_again_text_y,button_font,screen
    
    gameover = True


    while gameover:

        mousepos = pygame.mouse.get_pos()           

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if try_again_rect.collidepoint(mousepos):
                    game_active = True
                if quit_rect.collidepoint(mousepos):
                    pygame.quit()
                    exit()
                    
            if event.type == pygame.MOUSEMOTION:
                if try_again_rect.collidepoint(mousepos):
                    try_again_text = button_font.render("Try Again",True,'black')
                    screen.blit(try_again_surface,try_again_rect)
                    try_again_surface.blit(try_again_text, (try_again_text_x,try_again_text_y))
                    pygame.display.flip()
                else:
                    try_again_text = button_font.render("Try Again",True,'white')
                    screen.blit(try_again_surface,try_again_rect)
                    try_again_surface.blit(try_again_text, (try_again_text_x,try_again_text_y))
                    pygame.display.flip()
                if quit_rect.collidepoint(mousepos):
                    quit_text = button_font.render("Quit",True,'black')
                    screen.blit(quit_surface,quit_rect)
                    quit_surface.blit(quit_text,(quit_text_x,quit_text_y))
                    pygame.display.flip()
                else:
                    quit_text = button_font.render("Quit",True,'white')
                    screen.blit(quit_surface,quit_rect)
                    quit_surface.blit(quit_text, (quit_text_x,quit_text_y))
                    pygame.display.flip()

        screen.fill((94,129,162))
        screen.blit(game_over_text,(175,50))
        screen.blit(try_again_surface,try_again_rect)
        screen.blit(quit_surface,quit_rect)
        try_again_surface.fill("darkblue")
        quit_surface.fill("darkblue")
        try_again_surface.blit(try_again_text,(try_again_text_x,try_again_text_y))
        quit_surface.blit(quit_text,(quit_text_x,quit_text_y))

start()
pygame.quit()