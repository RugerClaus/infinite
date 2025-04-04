import pygame
from item import Item
import math
from projectile import Projectile

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
        self.projectile_image = pygame.image.load('graphics/Items/weapons/bulletforgame.png').convert_alpha()
        self.barrel_x = self.rect.right  # Default barrel position
        self.barrel_y = self.rect.centery
        

    def use(self):
        self.game.music_manager.play_sfx(self.name)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.barrel_x
        dy = mouse_y - self.barrel_y

        angle = math.degrees(math.atan2(dy, dx))


        projectile = Projectile(self.barrel_x,self.barrel_y, angle, 3, 5, self.projectile_image, self.game)
        self.game.projectiles.add(projectile)
        print(f"Firing from: ({self.barrel_x}, {self.barrel_y}) with angle: {angle}")


    def update_image(self, facing_right):
        self.image = self.image_right if facing_right else self.image_left

        if facing_right:
            self.game.player.active_weapon.barrel_x =self.rect.midright[0] - 5  # Adjust for accuracy
        else:
            self.game.player.active_weapon.barrel_x = self.rect.midleft[0] + 5   # Adjust for accuracy

        self.barrel_y = self.rect.centery  # Keep barrel vertically aligned

class LaserRifle(Weapon):
    def __init__(self, game):
        damage = 10
        self.name = "plasma_rifle"
        self.x = 800
        self.y = 700
        self.item_class = 'weapons'
        self.canonical_name = "Laser Rifle"
        self.pickup_sound = 'non_mechanical_item'

        # Set up the image and orientation
        self.image_right = pygame.image.load(f"graphics/Items/weapons/plasma_rifle_right.png").convert_alpha()
        self.image_left = pygame.image.load(f"graphics/Items/weapons/plasma_rifle_left.png").convert_alpha()
        self.image = self.image_right  # Default orientation

        super().__init__(self.x, self.y, self.name, game, damage,self.image_right,self.image_left)

    def update(self):
        super().update()

    def update_image(self, facing_right):
        super().update_image(facing_right)
            

    def use(self):
        super().use()

class RedLaserRifle(Weapon):
    def __init__(self, game):
        self.name = 'red_plasma_rifle'
        damage = 10
        self.x = 900
        self.y = 700
        self.item_class = 'weapons'
        self.canonical_name = "Red Laser Rifle"
        self.pickup_sound = 'non_mechanical_item'
        # Set up the image and orientation
        self.image_right = pygame.image.load(f"graphics/Items/weapons/red_plasma_rifle_right.png").convert_alpha()
        self.image_left = pygame.image.load(f"graphics/Items/weapons/red_plasma_rifle_left.png").convert_alpha()
        self.image = self.image_right  # Default orientation

        super().__init__(self.x, self.y, self.name, game, damage,self.image_right,self.image_left)
    def update(self):
        super().update()

    def update_image(self, facing_right):
        super().update_image(facing_right)

    def use(self):
        self.name = "plasma_rifle"
        super().use()

class Magnum(Weapon):
    def __init__(self, game):
        self.name = 'magnum'
        self.canonical_name = "Magnum"
        damage = 10
        self.x = 1000
        self.y = 700
        self.item_class = 'weapons'
        self.pickup_sound = 'mechanical_item'
        # Set up the image and orientation
        self.image_right = pygame.image.load(f"graphics/Items/weapons/magnum_right.png").convert_alpha()
        self.image_left = pygame.image.load(f"graphics/Items/weapons/magnum_left.png").convert_alpha()
        self.image = self.image_right  # Default orientation
        super().__init__(self.x, self.y, self.name, game, damage,self.image_right,self.image_left)

    def update(self):
        super().update()

    def update_image(self, facing_right):
        super().update_image(facing_right)
    
    def use(self):
        super().use()