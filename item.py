import pygame
from animate import Animation
from entity import Entity

class Item(Entity):
    def __init__(self, game, x, y, name, scrolls_with_background=False):
        super().__init__(game.screen,False,0)
        self.game = game
        self.name = name
        self.world_x = x
        self.world_y = y
        self.original_x = x
        self.is_in_hotbar = False
        self.path = "graphics/Items"
        self.image = None
        self.rect = None
        self.set_animation("idle", Animation([self.image], 10))
        self.collected = False
        self.scrolls_with_background = scrolls_with_background

    def update(self):
        super().update()

        if not self.collected:
            if self.scrolls_with_background:
                self.rect.x = self.original_x + self.game.background_x
                if self.rect.x + self.game.background_x > 0:
                    self.rect.x = self.original_x + self.game.background_x
            else:
                # If item doesn't scroll, it stays at its world position
                self.rect.x = self.world_x
                self.rect.y = self.world_y

    def collect(self):
        self.collected = True
        self.rect.x = -100
        self.rect.y = -100
        self.game.items.remove(self)
        
    
    def delete_self(self):
        if self in self.game.items:
            self.game.items.remove(self)
        del self  # Python will clean up if no references remain