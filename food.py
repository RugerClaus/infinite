from item import Item
import pygame
from random import randint

class Food(Item):
    def __init__(self, x, y, name, game, nutrition_value):
        super().__init__(game,x,y,name,True)
        self.image = pygame.image.load(f"{self.path}/food/{name}.png")
        self.rect = self.image.get_rect(bottomleft  = (x,y))
        self.nutrition_value = nutrition_value
        self.is_stackable = True
        self.stack_size = 1

class Apple(Food):
    def __init__(self, game):
        self.name = "apple"
        x = randint(500,2500) 
        y = 700
        super().__init__(x, y, self.name,game, nutrition_value=10)

    def draw(self):
        super().draw()

    def update(self):
        super().update()
