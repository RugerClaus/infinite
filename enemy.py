import pygame
from animate import Animation
from entity import Entity

class Enemy(Entity):
    def __init__(self,x,y,game,player,enemy_type):
        super().__init__(x,y,72,36,game.screen)
        self.game = game
        self.player = player
        self.world_x = x
        self.world_y = y
        self.music_manager = game.music_manager
        self.speed = 3
        self.type = enemy_type

        if self.type == 'snail':
            self.enemy_frames = [
            pygame.image.load("graphics/snail/snail_1.png").convert_alpha(),
            pygame.image.load("graphics/snail/snail_2.png").convert_alpha()
            ]
        self.animation = Animation(self.enemy_frames,10)
        self.image = self.enemy_frames[0]
        self.rect = self.image.get_rect(bottomleft = (x,y))
        

    def update(self):

        self.rect.x = self.world_x + self.game.background_x

        if self.player:
            if self.rect.x > self.player.rect.x:
                self.world_x -= self.speed
            else:
                self.world_x -= self.speed
        
        if self.world_x <= 0:
            self.world_x = 1000

        self.animation.update()
        self.image = self.animation.get_current_frame()

    def draw(self):
        super().draw()