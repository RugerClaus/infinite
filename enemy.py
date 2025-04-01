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
        self.speed = 0 #will change back to 3 later when working on enemy logic. for now I'm not moving the enemy and am going to focus on item/inventory system
        self.type = enemy_type

        if self.type == 'snail':
            self.enemy_frames = [
            pygame.image.load("graphics/snail/snail_1.png").convert_alpha(),
            pygame.image.load("graphics/snail/snail_2.png").convert_alpha()
            ]
        self.animation = Animation(self.enemy_frames,10)
        self.image = self.enemy_frames[0]
        self.rect = self.image.get_rect(midbottom = (x,y))
        

    def update(self):
        super().update()
        self.rect.x = self.world_x + self.game.background_x

        if self.rect.bottom >= 701:
            self.rect.bottom = 700  # Ground level
            self.gravity = 0

        if self.player:
            self.world_x -= self.speed
        
        if self.world_x <= 0:
            self.world_x = 1000
        if self.world_x + self.rect.width < self.player.rect.x:
            self.player.passed_enemy = True
        elif self.world_x > self.player.rect.x:
            self.player.passed_enemy = False
        
        if self.speed == 0:
            self.image = self.enemy_frames[0]
        else:
            self.image = self.animation.get_current_frame()
        self.animation.update()

    def draw(self):
        super().draw()