import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,game):
        super().__init__()

        self.x = x
        self.y = y
        self.game = game
        self.screen = game.screen
        self.music_manager = game.music_manager

        



