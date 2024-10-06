import pygame
from sys import exit
from constants import *

pygame.init()

pygame.display.set_caption("Ass")

run = True

def game_over():
    global score,speed,game_active,game_over_font,quit_text_x,quit_text_y,try_again_text_x,try_again_text_y,player_rect

    try_again_surface = pygame.Surface((200,50))
    try_again_text = button_font.render("Try Again",True,'white')
    try_again_rect = try_again_surface.get_rect(center = (200,200))
    quit_surface = pygame.Surface((200,50))
    quit_text = button_font.render("Quit",True,'white')
    quit_rect = try_again_surface.get_rect(center = (600,200))
    game_over_text = game_over_font.render("Game Over!",True,(255,255,255))

    
    menu = True


    while menu:

        mousepos = pygame.mouse.get_pos()           

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if try_again_rect.collidepoint(mousepos):
                    print('clicked')
                    game_active = True
                    snail_rect.left = 800
                    speed = 0
                    score = 0
                    player_x = 20
                    main()
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

        pygame.display.flip()
    pygame.quit()


def main():
    global game_active,score,player_gravity,player_x,speed
    while run:
        milli = pygame.time.get_ticks()

        mousepos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if game_active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mousepos[0] > player_x:
                        speed = 2
                    if mousepos[0] < player_x:
                        speed = -2
                    if mousepos[1] > player_rect.top and player_rect.top > 0:
                        player_gravity = -8.5
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    snail_rect.left = 800
                    player_rect.left = 20
                    speed = 0
                    score = 0
                    
        if game_active:
            screen.fill("black")
            score_surface = font.render(f'Score: {score}',True,(64,64,64))
            screen.blit(sky_surface,(0,0))
            screen.blit(ground_surface,(0,300))
            screen.blit(score_surface,(650,5))

            snail_rect.x -= 5
            if snail_rect.right <= 0: snail_rect.left = 800
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
                player_gravity = -10
            if snail_rect.colliderect(player_rect):
                game_active = False

            if player_rect.right > snail_rect.left and not passed_snail:
                passed_snail = True
                score += 1
            if snail_rect.left > player_rect.right:
                passed_snail = False
            if milli > 3000:
                screen.blit(tree_1_surface,tree_1_rect)
                tree_1_rect.x -= scroll_speed
                if tree_1_rect.left < -100:
                    tree_1_rect.right = 1000
                screen.blit(tree_2_surface,tree_2_rect)
                tree_2_rect.x -= scroll_speed
                if tree_2_rect.left < -100:
                    tree_2_rect.right = 1100
        else:
            pygame.display.flip()
            game_over()
            break
        pygame.display.flip()
        clock.tick(60)
main()
pygame.quit()