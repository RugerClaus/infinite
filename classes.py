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
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('font/Pixeltype.ttf',50)
        self.pause_font = pygame.font.Font('font/Pixeltype.ttf',40)
        self.button_font = pygame.font.Font('font/Roboto-Black.ttf',30)
        self.button_fontgame_over_font = pygame.font.Font('font/gameover.ttf',50)

    def reset_game(self):
        self.score = 0
        self.snail_rect.x = 800
        self.player_rect.x = 20
        self.game_active = True

    def render_main_menu(self):
        button_color = (255,120,0)
        play_button = Button("Play!",400,100,100,50,self.button_font,button_color,self.start_game)
        options_button = Button("Options",400,200,100,50,self.button_font,button_color,self.quit_game)

    def start_game():
        print('Game started!')
        
    def quit_game():
        print("Goodbye!")
        pygame.quit()
        ex()

class Button():
    def __init__(self,text,x,y,width,height,font,color,action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.action = action
        self.color = color

        self.surface = pygame.Surface((self.width,self.height))
        self.text_surface = self.font.render(self.text,True,self.color)
        self.text_rect = self.text_surface.get_rect(center=(self.x+self.width//2,self.y+self.height//2))
        self.rect = self.surface.get_rect(center = (self.x,self.y))

    def draw(self,screen,mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen,(0,0,0),self.rect)
        else:
            pygame.draw.rect(screen,(0,128,0), self.rect)

    def is_clicked(self,mouse_pos,mouse_click):
        if self.rect.collidepoint(mouse_pos) and mouse_click:
            if self.action:
                self.action()