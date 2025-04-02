import pygame
from item import Item

class Weapon(Item):
    def __init__(self,x,y,name,game,damage):
        super().__init__(x,y,name,game)
        self.damage = damage
        self.image = pygame.image.load(f"{self.path}/weapons/{self.name}.png")
        self.rect = self.image.get_rect(bottomleft  = (x,y))

class Baton(Weapon):
    def __init__(self,game):
        name = 'baton'
        x,y = 800,700
        damage = 2
        super().__init__(x,y,name,game,damage)
