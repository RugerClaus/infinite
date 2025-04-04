import pygame
from animate import Animation
from entity import Entity

class Enemy(Entity):
    def __init__(self,x,y,game,player):
        super().__init__(game.screen,True,5)
        self.game = game
        self.player = player
        self.world_x = x
        self.world_y = y
        self.music_manager = game.music_manager
        self.speed = 0 #will change back to 3 later when working on enemy logic. for now I'm not moving the enemy and am going to focus on item/inventory system
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
import pygame
from enemy import Enemy

class Snail(Enemy):
    def __init__(self, game, player):
        # Load snail animation frames
        x=2000
        self.enemy_frames = [
            pygame.image.load("graphics/snail/snail_1.png").convert_alpha(),
            pygame.image.load("graphics/snail/snail_2.png").convert_alpha()
        ]

        super().__init__(x, 700, game, player)

        self.speed = 2
        self.health = 3
        self.damage = 1
        self.name = "snail"

    def update(self):
        super().update()
        if self.health <= 0:
            print(f"Killed {self.name}")
            self.kill()
        # Optional: Add snail-specific logic here (e.g., play squish sound on death)
