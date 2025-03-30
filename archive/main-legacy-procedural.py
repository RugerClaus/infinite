import pygame
from sys import exit
from archive.constants import *
from archive.magic import tree_magic, enemy_magic

pygame.init()

pygame.display.set_caption("Ass")

def shutdown():
    print('Shutdown. Bye bye...')
    pygame.quit()
    exit()

def game_over():
    global score,speed,game_active,game_over_font,main,player_x,tryagaincount,player_gravity,alive

    try_again_surface = pygame.Surface((200,50))
    try_again_text = button_font.render("Try Again",True,'white')
    try_again_rect = try_again_surface.get_rect(center = (200,200))
    quit_surface = pygame.Surface((200,50))
    quit_text = button_font.render("Quit",True,'white')
    quit_rect = try_again_surface.get_rect(center = (600,200))
    quittodesktop_surface = pygame.Surface((200,50))
    quittodesktop_text = button_font.render("Exit",True,'white')
    quittodesktop_rect = quittodesktop_surface.get_rect(center = (400,300))
    game_over_text = game_over_font.render("Game Over!",True,'red')

    try_again_text_rect = try_again_text.get_rect(center = try_again_rect.center)
    quit_text_rect = quit_text.get_rect(center = quit_rect.center)
    quittodesktop_text_rect = quittodesktop_text.get_rect(center = quittodesktop_rect.center)

    
    gameover = True


    while gameover:

        mousepos = pygame.mouse.get_pos()           

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shutdown()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if try_again_rect.collidepoint(mousepos):
                    tryagaincount += 1
                    print(f"Try Again Count: {tryagaincount}")
                    game_active = True
                    alive = True
                    snail_rect.left = 800
                    speed = 0
                    score = 0
                    player_x = 20
                    player_gravity = 0
                    main()
                if quittodesktop_rect.collidepoint(mousepos):
                    shutdown()
                if quit_rect.collidepoint(mousepos):
                    snail_rect.left = 800
                    speed = 0
                    score = 0
                    player_x = 20
                    start()

                    
            if event.type == pygame.MOUSEMOTION:
                if try_again_text_rect.collidepoint(mousepos):
                    try_again_text = button_font.render("Try Again",True,'black')
                    screen.blit(try_again_surface,try_again_rect)
                    try_again_surface.blit(try_again_text, try_again_text_rect)
                    pygame.display.flip()
                else:
                    try_again_text = button_font.render("Try Again",True,'white')
                    screen.blit(try_again_surface,try_again_rect)
                    try_again_surface.blit(try_again_text, try_again_text_rect)
                    pygame.display.flip()
                if quit_text_rect.collidepoint(mousepos):
                    quit_text = button_font.render("Quit",True,'black')
                    screen.blit(quit_surface,quit_rect)
                    quit_surface.blit(quit_text,quit_text_rect)
                    pygame.display.flip()
                else:
                    quit_text = button_font.render("Quit",True,'white')
                    screen.blit(quit_surface,quit_rect)
                    quit_surface.blit(quit_text, quit_text_rect)
                    pygame.display.flip()
                if quittodesktop_text_rect.collidepoint((mousepos)):
                    quittodesktop_text = button_font.render('Exit',True,'black')
                    screen.blit(quittodesktop_surface,quittodesktop_rect)
                    quittodesktop_surface.blit(quittodesktop_text,quittodesktop_text_rect)
                    pygame.display.flip()
                else:
                    quittodesktop_text = button_font.render("Exit",True,"white")
                    screen.blit(quittodesktop_surface,quittodesktop_rect)
                    quit_surface.blit(quittodesktop_text, quittodesktop_text_rect)
                    pygame.display.flip()

        try_again_surface.fill("darkblue")
        quit_surface.fill("darkblue")
        quittodesktop_surface.fill("darkblue")
        screen.blit(game_over_text,(175,50))
        screen.blit(try_again_surface,try_again_rect)
        screen.blit(quit_surface,quit_rect)
        screen.blit(quittodesktop_surface,quittodesktop_rect)
        screen.blit(try_again_text,try_again_text_rect)
        screen.blit(quittodesktop_text,quittodesktop_text_rect)
        screen.blit(quit_text,quit_text_rect)

        pygame.display.flip()
    pygame.quit()


def pause_game():
    global screen,pausebuttonsize,speed,score,player_x,game_active

    #resume button
    resume_surface = pygame.Surface(pausebuttonsize)
    resume_button_rect = resume_surface.get_rect(center = (100,50))
    resume_button_text = pause_font.render("Resume",True,'lightblue')
    resume_button_text_rect = resume_button_text.get_rect(center = resume_button_rect.center)

    #options button
    options_surface = pygame.Surface(pausebuttonsize)
    options_button_rect = options_surface.get_rect(center = (100,125))
    options_button_text = pause_font.render("Options",True,'lightblue')
    options_button_text_rect = options_button_text.get_rect(center = options_button_rect.center)   

    #main menu button
    quittomenu_surface = pygame.Surface(pausebuttonsize)
    quittomenu_button_rect = options_surface.get_rect(center = (100,200))
    quittomenu_button_text = pause_font.render("Menu",True,'lightblue')
    quittomenu_button_text_rect = quittomenu_button_text.get_rect(center = quittomenu_button_rect.center)

    #exit button
    quittodesktop_surface = pygame.Surface(pausebuttonsize)
    quittodesktop_button_rect = quittodesktop_surface.get_rect(center = (100,275))
    quittodesktop_button_text = pause_font.render("Exit",True,'lightblue')
    quittodesktop_button_text_rect = quittodesktop_button_text.get_rect(center = quittodesktop_button_rect.center)   

    paused = True
    while paused:

        mousepos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shutdown()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                #debug
                if event.key == pygame.K_q:
                    start()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button_rect.collidepoint(mousepos):
                    paused = False
                if options_button_rect.collidepoint(mousepos):
                    print("Not started yet")
                if quittomenu_button_rect.collidepoint(mousepos):
                    snail_rect.left = 800
                    speed = 0
                    score = 0
                    player_x = 20
                    game_active = False
                    start()
                if quittodesktop_button_rect.collidepoint(mousepos):
                    shutdown()
            if event.type == pygame.MOUSEMOTION:
                if resume_button_rect.collidepoint(mousepos):
                    resume_button_text = pause_font.render("Resume",True,'white')
                    screen.blit(resume_surface,resume_button_rect)
                    screen.blit(resume_button_text,resume_button_text_rect)
                else:
                    resume_button_text = pause_font.render("Resume",True,'lightblue')
                    screen.blit(resume_surface,resume_button_rect)
                    screen.blit(resume_button_text,resume_button_text_rect)
                if options_button_rect.collidepoint(mousepos):
                    options_button_text = pause_font.render("Options",True,'white')
                    screen.blit(options_surface,options_button_rect)
                    screen.blit(options_button_text,options_button_text_rect)
                else:
                    options_button_text = pause_font.render("Options",True,'lightblue')
                    screen.blit(options_surface,options_button_rect)
                    screen.blit(options_button_text,options_button_text_rect)
                if quittomenu_button_rect.collidepoint(mousepos):
                    quittomenu_button_text = pause_font.render("Menu",True,'white')
                    screen.blit(quittomenu_surface,quittomenu_button_rect)
                    screen.blit(quittomenu_button_text,quittomenu_button_text_rect)
                else:
                    quittomenu_button_text = pause_font.render("Menu",True,'lightblue')
                    screen.blit(quittomenu_surface,quittomenu_button_rect)
                    screen.blit(quittomenu_button_text,quittomenu_button_text_rect)
                if quittodesktop_button_rect.collidepoint(mousepos):
                    quittodesktop_button_text = pause_font.render("Exit",True,'white')
                    screen.blit(quittodesktop_surface,quittodesktop_button_rect)
                    screen.blit(quittodesktop_button_text,quittodesktop_button_text_rect)
                else:
                    quittodesktop_button_text = pause_font.render("Exit",True,'lightblue')
                    screen.blit(quittodesktop_surface,quittodesktop_button_rect)
                    screen.blit(quittodesktop_button_text,quittodesktop_button_text_rect)
                

        screen.blit(resume_surface,resume_button_rect)
        screen.blit(resume_button_text,resume_button_text_rect)
        screen.blit(options_surface,options_button_rect)
        screen.blit(options_button_text,options_button_text_rect)
        screen.blit(quittomenu_surface,quittomenu_button_rect)
        screen.blit(quittomenu_button_text,quittomenu_button_text_rect)
        screen.blit(quittodesktop_surface,quittodesktop_button_rect)
        screen.blit(quittodesktop_button_text,quittodesktop_button_text_rect)
        clock.tick(60)
        pygame.display.flip()

def player_logic():
    global player_gravity,game_active,player_x,speed,passed_snail,score,alive

    player_x += speed
    player_rect.x = player_x
    if player_rect.bottom > 299 and alive: 
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
        alive = False
        snail_rect.x = 4000
        speed = 0
        player_gravity -= 7.5
        player_gravity += 2
    if player_rect.top >= 400:
        snail_rect.left = 800
        speed = 0
        score = 0
        player_x = 20
        tree_1_rect.x = 1000
        tree_2_rect.x = 1500
        game_over()
        

    if player_rect.right > snail_rect.left and not passed_snail:
        passed_snail = True
        score += 1
    if snail_rect.left > player_rect.right:
        passed_snail = False

def main():
    global game_active,score,player_gravity,player_x,speed,game_over
    game_active = True
    while game_active:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shutdown()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and speed <= 0:
                    speed = 2
                if event.key == pygame.K_a and speed == 2:
                    speed = -2
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -8.5
                if event.key == pygame.K_ESCAPE:
                    pause_game()
                    
        score_surface = font.render(f'Score: {score}',True,(64,64,64))
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        screen.blit(score_surface,(650,5))

        tree_1_rect.x -= 1
        tree_2_rect.x -= 1
        tree_1_rect.bottom = 300
        tree_2_rect.bottom = 300
        if tree_1_rect.right <= 0: 
            tree_magic(tree_1_rect)
        if tree_2_rect.right <= 0: 
            tree_magic(tree_2_rect)
        screen.blit(tree_1_surface,tree_1_rect)
        screen.blit(tree_2_surface,tree_2_rect)

        snail_rect.x -= 3
        if snail_rect.right <= 0: snail_rect.left = 800
        screen.blit(snail_surface,snail_rect)

        player_gravity += 0.2
        player_rect.bottom += player_gravity #creates the gravity effect
        screen.blit(player_surface,player_rect)

        player_logic()
        pygame.display.flip()
        clock.tick(60)
        
def start():

    global score,speed,game_over_font,button_font,font,main,player_x

    

    
    play_surface = pygame.Surface((100,50))
    play_button_rect = play_surface.get_rect(center = (400,100))
    play_button_text = button_font.render("Play!",True,'white')
    quit_surface = pygame.Surface((100,50))
    quit_button_rect = quit_surface.get_rect(center = (400,200))
    quit_button_text = button_font.render("Quit",True,'white')
    play_button_text_rect = play_button_text.get_rect(center = play_button_rect.center)
    quit_button_text_rect = quit_button_text.get_rect(center = quit_button_rect.center)

    menu = True

    while menu:
        mousepos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shutdown()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(mousepos):
                    print('Play game!')
                    snail_rect.left = 800
                    speed = 0
                    score = 0
                    player_x = 20
                    main()
                    pygame.display.flip()
                if quit_button_text_rect.collidepoint(mousepos):
                    shutdown()
                
            if event.type == pygame.MOUSEMOTION:
                if play_button_rect.collidepoint(mousepos):
                    play_button_text = button_font.render("Play!",True,(255,120,0))
                    screen.blit(play_surface,play_button_rect)
                    screen.blit(play_button_text, play_button_text_rect)
                    pygame.display.flip()
                else:
                    play_button_text = button_font.render("Play!",True,'white')
                    screen.blit(play_surface,play_button_rect)
                    screen.blit(play_button_text, play_button_text_rect)
                    pygame.display.flip()
                if quit_button_rect.collidepoint(mousepos):
                    quit_button_text = button_font.render("Quit",True,(255,120,0))
                    screen.blit(quit_surface,quit_button_rect)
                    screen.blit(quit_button_text, quit_button_text_rect)
                    pygame.display.flip()
                else:
                    quit_button_text = button_font.render("Quit",True,'white')
                    screen.blit(quit_surface,quit_button_rect)
                    screen.blit(quit_button_text, quit_button_text_rect)
                    pygame.display.flip()
            #debugging
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F9:
                    print('what you want to print')
                if event.key == pygame.K_F1:
                    snail_rect.left = 800
                    speed = 0
                    score = 0
                    player_x = 20
                    main()

            screen.fill((255,128,0))
            screen.blit(play_surface,play_button_rect)
            screen.blit(play_button_text, play_button_text_rect)
            screen.blit(quit_surface,quit_button_rect)
            screen.blit(quit_button_text,quit_button_text_rect)
        pygame.display.flip()
        clock.tick(60)
start()
    
pygame.quit()