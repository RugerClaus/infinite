import pygame
import random
from sys import exit as ex

#Window class
class Window():
    def __init__(self,width,height,title="Juggernot 5k"):
        pygame.init()
        pygame.font.init()
        self.width = width
        self.height = height
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.font = pygame.font.Font('font/Pixeltype.ttf',50)
        self.button_font = pygame.font.Font('font/Roboto-Black.ttf',30)
        self.button_fontgame_over_font = pygame.font.Font('font/gameover.ttf',50)

        self.music_active = False
        self.sfx_active = False
        self.game_active = False
        self.window_state = 'main_menu'

    def render_main_menu(self):
        self.window_state = 'main_menu'
        button_unhovered_color = "orange"
        button_hovered_color = "white"


        play_button = Button("Play!",400,100,125,50,self.button_font,button_unhovered_color,button_hovered_color,self.start_game)
        options_button = Button("Options",400,200,125,50,self.button_font,button_unhovered_color,button_hovered_color,self.render_options_menu)
        quit_button = Button("Exit",400,300,125,50,self.button_font,button_unhovered_color,button_hovered_color,self.quit_game)

        self.screen.fill((255, 128, 0))
        play_button.draw(self.screen, pygame.mouse.get_pos())
        options_button.draw(self.screen,pygame.mouse.get_pos())
        quit_button.draw(self.screen, pygame.mouse.get_pos())

        pygame.display.flip()

        # Event loop for menu screen
        self.handle_ui_events([play_button,options_button,quit_button])

    def render_options_menu(self):
        self.window_state = 'options_menu'
        button_unhovered_color = "orange"
        button_hovered_color = "white"

        #buttons
        back_button = Button("Back",400,300,100,50,self.button_font,button_unhovered_color,button_hovered_color,self.render_main_menu)

        self.screen.fill((255, 128, 0))
        back_button.draw(self.screen,pygame.mouse.get_pos())
        
        pygame.display.flip()

        self.handle_ui_events([back_button])

    def handle_ui_events(self, buttons):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        button.is_clicked(pygame.mouse.get_pos(), event.button == 1)
                elif event.type == pygame.MOUSEMOTION:  # Ensure buttons update on hover
                    return  # Break the loop and refresh the buttons

                    
        

    def start_game(self):
        self.window_state = 'in_game'
        game = Game(True,self.screen,self.clock,self)
        game.game_loop()

    def quit_game(self):
        print("Goodbye!")
        pygame.quit()
        ex()

    def toggle_music(self):
        if self.music_active == True:
            self.music_active == False
        else:
            self.music_active = True
    
    def toggle_sfx(self):
        if self.sfx_active == True:
            self.sfx_active = False
        else:
            self.sfx_active = True

    def main_loop(self):
        while self.running:
                
            if self.window_state == "main_menu":
                self.render_main_menu()
            elif self.window_state == 'options_menu':
                self.render_options_menu()
            elif self.window_state == "in_game":
                self.start_game()
                

            self.clock.tick(60)


class Button():
    def __init__(self,text,x,y,width,height,font,text_unhovered_color,text_hovered_color,action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.action = action
        self.text_unhovered_color = text_unhovered_color
        self.text_hovered_color = text_hovered_color
        self.color = "black"
        

        self.surface = pygame.Surface((self.width,self.height))
        self.text_surface = self.font.render(self.text,True,self.text_unhovered_color)
        self.rect = self.surface.get_rect(center = (self.x,self.y))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):  
            text_color = self.text_hovered_color  # Use hovered color when mouse is over
        else:
            text_color = self.text_unhovered_color  # Use unhovered color otherwise

        self.text_surface = self.font.render(self.text, True, text_color)

        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self,mouse_pos,mouse_click):
        if self.rect.collidepoint(mouse_pos) and mouse_click:
            if self.action:
                self.action()
                

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.speed = 0
        self.gravity = 0
        self.sprites_surfaces = [
            pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha(),
            pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        ]
        self.x,self.y = (20,300)
        for sprite in self.sprites_surfaces:
            self.rect = sprite.get_rect(bottomleft=(self.x,self.y))
    
    def update(self):
        for i in self.sprites:
            pass


class Game():
    def __init__(self,game_active,screen,clock,window):
        self.paused = False
        self.game_active = game_active
        self.pause_button_font = pygame.font.Font('font/Pixeltype.ttf',40)
        self.score_font = pygame.font.Font('font/Pixeltype.ttf',50)
        self.score = 0
        self.clock = clock
        self.window = window
        self.screen = screen
        self.player = Player()
        self.check_state()

    def check_state(self):
        if self.game_active == True:
            self.game_loop()
        else:
            self.window.render_main_menu()

    def exit(self):
        self.window.quit_game()
    
    def reset(self):
        self.score = 0
        self.player.reset()

    def render_pause_menu(self):
        self.paused = True
        resume_button = Button("Resume",100,75,100,50,self.pause_button_font,(173, 216, 230),(255, 255, 255),self.update_pause_state)
        quittomenu_button = Button("Menu",100,150,100,50,self.pause_button_font,(173, 216, 230),(255, 255, 255),self.go_to_main_menu)
        quittodesktop_button = Button("Exit",100,220,100,50,self.pause_button_font,(173, 216, 230),(255, 255, 255),self.exit)
        
        buttons = [resume_button, quittomenu_button, quittodesktop_button]

        for button in buttons:
            button.draw(self.screen, pygame.mouse.get_pos())

        pygame.display.flip()

        return buttons
    
    def go_to_main_menu(self):
        self.paused = False
        self.game_active = False
        self.window.window_state = 'main_menu'

    def update_pause_state(self):
        self.paused = not self.paused

    def render_environment(self):
        score_surface = self.score_font.render(f'Score: {self.score}',True,(64,64,64))
        sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
        ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
        self.screen.blit(sky_surface,(0,0))
        self.screen.blit(ground_surface,(0,300))
        self.screen.blit(score_surface,(650,5))
    
    def handle_player_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and self.player.speed <= 0:
                    self.player.speed = 2
                if event.key == pygame.K_a and self.player.speed == 2:
                    self.player.speed = -2
                if event.key == pygame.K_SPACE and self.player.rect.bottom == 300:
                    self.player.gravity = -8.5
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused

    def game_loop(self):

        while self.game_active:

            self.handle_player_input()

            if self.paused:
                pause_buttons = self.render_pause_menu()
                while self.paused:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in pause_buttons:
                        button.draw(self.screen,mouse_pos)
                    pygame.display.flip()
                    self.window.handle_ui_events(pause_buttons)
            
            else: self.render_environment()

            # render_player()

            # tree_1_rect.x -= 1
            # tree_2_rect.x -= 1
            # tree_1_rect.bottom = 300
            # tree_2_rect.bottom = 300
            # if tree_1_rect.right <= 0: 
            #     tree_magic(tree_1_rect)
            # if tree_2_rect.right <= 0: 
            #     tree_magic(tree_2_rect)
            # screen.blit(tree_1_surface,tree_1_rect)
            # screen.blit(tree_2_surface,tree_2_rect)

            # snail_rect.x -= 3
            # if snail_rect.right <= 0: snail_rect.left = 800
            # screen.blit(snail_surface,snail_rect)

            # player_gravity += 0.2
            # player_rect.bottom += player_gravity #creates the gravity effect
            # screen.blit(player_surface,player_rect)

            
            pygame.display.flip()
            self.clock.tick(60)


window = Window(800,400,"Fuck Me!")
window.main_loop()