import pygame
from item import Item

class Weapon(Item):
    def __init__(self,x,y, name, game,damage):
        super().__init__(game,x,y,name,True)
        self.image = pygame.image.load(f"{self.path}/weapons/{name}.png")
        self.rect = self.image.get_rect(bottomleft  = (x,y))
        self.is_stackable = False
        self.stack_size = 1
        self.damage = damage

class Baton(Weapon):
    def __init__(self,game):
        damage = 10
        self.name = "baton"
        self.x = 800
        self.y = 700
        super().__init__(self.x,self.y,self.name,game,damage)

    def draw(self):
        super().draw()

    def update(self):
        super().update()
