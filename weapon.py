import pygame
from item import Item
from sound import SoundManager

class Weapon(Item):
    def __init__(self,x,y, name, game,damage):
        super().__init__(game,x,y,name,True)
        self.is_stackable = False
        self.stack_size = 1
        self.damage = damage


class LaserRifle(Weapon):
    def __init__(self,game):
        damage = 10
        self.name = "plasma_rifle"
        self.x = 800
        self.y = 700
        self.image_right = pygame.image.load(f"graphics/Items/weapons/plasma_rifle_right.png").convert_alpha()
        self.image_left = pygame.image.load(f"graphics/Items/weapons/plasma_rifle_left.png").convert_alpha()
        self.image = self.image_right
        super().__init__(self.x,self.y,self.name,game,damage)

    def draw(self):
        super().draw()

    def update(self):
        super().update()
    def update_image(self, facing_right):
        self.image = self.image_right if facing_right else self.image_left
    def use(self):
        self.game.music_manager.play_sfx("plasma_rifle")

class RedLaserRifle(LaserRifle):
    def __init__(self, game):
        super().__init__(game)
        self.image_left = pygame.image.load(f"graphics/Items/weapons/red_plasma_rifle_left.png").convert_alpha()
        self.image_right = pygame.image.load(f"graphics/Items/weapons/red_plasma_rifle_right.png").convert_alpha()
        self.image= self.image_right