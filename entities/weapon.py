import pygame
from entities.item import Item
import math
from entities.projectile import Projectile

class Weapon(Item):
    def __init__(self, x, name, game, damage,image_right,image_left,bullet_speed,sound):
        self.image_right = image_right
        self.image_left = image_left
        self.sound = sound
        self.item_class = 'weapons'
        y=650
        super().__init__(game, x, y, name, self.item_class, True)
        self.is_stackable = False
        self.stack_size = 1
        self.damage = damage
        self.original_x = x
        self.projectile_image = pygame.image.load(f'graphics/Items/weapons/bullet_for_{self.name}.png').convert_alpha()
        self.barrel_x = self.rect.right
        self.barrel_y = self.rect.centery
        self.bullet_speed = bullet_speed


    def use(self):
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.barrel_x
        dy = mouse_y - self.barrel_y

        angle = math.degrees(math.atan2(dy, dx))


        projectile = Projectile(self.barrel_x,self.barrel_y, angle, self.bullet_speed, self.damage, self.projectile_image, self.game)
        self.game.projectiles.add(projectile)
        print(f"Firing from: ({self.barrel_x}, {self.barrel_y}) with angle: {angle}")
        self.game.music_manager.play_sfx(self.sound)

    def update_image(self, facing_right):
        self.image = self.image_right if facing_right else self.image_left
        # pygame.draw.line(self.game.screen, (0, 255, 0), (self.barrel_x, self.barrel_y), pygame.mouse.get_pos(), 1) #draws a line from the center of the gun to mousepos

class LaserRifle(Weapon):
    def __init__(self, game):
        damage = 10
        self.name = "plasma_rifle_blue"
        self.sound = "plasma_rifle"
        self.x = 500
        self.item_class = 'weapons'
        self.canonical_name = "Laser Rifle"
        self.pickup_sound = 'non_mechanical_item'
        self.bullet_speed = 5
        # Set up the image and orientation
        self.image_right = pygame.image.load(f"graphics/Items/weapons/plasma_rifle_blue_right.png").convert_alpha()
        self.image_left = pygame.image.load(f"graphics/Items/weapons/plasma_rifle_blue_left.png").convert_alpha()
        self.image = self.image_right  # Default orientation

        super().__init__(self.x, self.name, game, damage,self.image_right,self.image_left,self.bullet_speed,self.sound)

    def update(self):
        super().update()

    def update_image(self, facing_right):
        super().update_image(facing_right)
            

    def use(self):
        super().use()

class RedLaserRifle(Weapon):
    def __init__(self, game):
        self.name = 'plasma_rifle_red'
        damage = 15
        self.x = 600
        self.sound = "plasma_rifle"
        self.item_class = 'weapons'
        self.canonical_name = "Red Laser Rifle"
        self.pickup_sound = 'non_mechanical_item'
        self.bullet_speed = 5
        # Set up the image and orientation
        self.image_right = pygame.image.load(f"graphics/Items/weapons/plasma_rifle_red_right.png").convert_alpha()
        self.image_left = pygame.image.load(f"graphics/Items/weapons/plasma_rifle_red_left.png").convert_alpha()
        self.image = self.image_right  # Default orientation

        super().__init__(self.x, self.name, game, damage,self.image_right,self.image_left,self.bullet_speed,self.sound)
    def update(self):
        super().update()

    def update_image(self, facing_right):
        super().update_image(facing_right)

    def use(self):
        super().use()

class Magnum(Weapon):
    def __init__(self, game):
        self.name = 'magnum'
        self.sound = "magnum"
        self.canonical_name = "Magnum"
        damage = 15
        self.x = 700
        self.item_class = 'weapons'
        self.pickup_sound = 'mechanical_item'
        # Set up the image and orientation
        self.image_right = pygame.image.load(f"graphics/Items/weapons/magnum_right.png").convert_alpha()
        self.image_left = pygame.image.load(f"graphics/Items/weapons/magnum_left.png").convert_alpha()
        self.image = self.image_right  # Default orientation
        self.bullet_speed = 10
        super().__init__(self.x, self.name, game, damage,self.image_right,self.image_left,self.bullet_speed,self.sound)

    def update(self):
        super().update()

    def update_image(self, facing_right):
        super().update_image(facing_right)
    
    def use(self):
        super().use()