import pygame
from animate import Animation
from entity import Entity

class Item(Entity):
    def __init__(self, x, y, width, height, name, game):
        super().__init__(x, y, width, height, game.screen)
        self.game = game
        self.name = name
        self.original_x = x
        self.original_y = y
        #self.velocity_x = velocity_x
        #self.velocity_y = velocity_y
        #self.angular_velocity = angular_velocity 
        self.image = pygame.image.load(f"graphics/Items/{name}.png")
        self.rect = self.image.get_rect(bottomleft = (x,y))

    def update(self):
        self.rect.x = self.original_x + self.game.background_x

    def draw(self):
        super().draw()