import pygame
from item import Item

class Weapon(Item):
    def __init__(self, x, y, name, game, damage,image_right,image_left):
        self.image_right = image_right
        self.image_left = image_left
        self.item_class = 'weapons'
        super().__init__(game, x, y, name, self.item_class, True)
        self.is_stackable = False
        self.stack_size = 1
        self.damage = damage
        self.original_x = x

class LaserRifle(Weapon):
    def __init__(self, game):
        damage = 10
        self.name = "plasma_rifle"
        self.x = 800
        self.y = 700
        self.item_class = 'weapons'

        # Set up the image and orientation
        self.image_right = pygame.image.load(f"graphics/Items/weapons/plasma_rifle_right.png").convert_alpha()
        self.image_left = pygame.image.load(f"graphics/Items/weapons/plasma_rifle_left.png").convert_alpha()
        self.image = self.image_right  # Default orientation

        super().__init__(self.x, self.y, self.name, game, damage,self.image_right,self.image_left)

    def update(self):
        super().update()

    def update_image(self, facing_right):
        self.image = self.image_right if facing_right else self.image_left

    def use(self):
        self.game.music_manager.play_sfx("plasma_rifle")

class RedLaserRifle(Weapon):
    def __init__(self, game):
        self.name = 'red_plasma_rifle'
        damage = 10
        self.x = 1500
        self.y = 700
        self.item_class = 'weapons'

        # Set up the image and orientation
        self.image_right = pygame.image.load(f"graphics/Items/weapons/red_plasma_rifle_right.png").convert_alpha()
        self.image_left = pygame.image.load(f"graphics/Items/weapons/red_plasma_rifle_left.png").convert_alpha()
        self.image = self.image_right  # Default orientation

        super().__init__(self.x, self.y, self.name, game, damage,self.image_right,self.image_left)

    def update(self):
        super().update()

    def update_image(self, facing_right):
        self.image = self.image_right if facing_right else self.image_left

    def use(self):
        self.game.music_manager.play_sfx("plasma_rifle")