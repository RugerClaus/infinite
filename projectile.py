import pygame
import math
from entity import Entity

class Projectile(Entity):
    def __init__(self,x,y,angle,speed,damage,image,game):
        super().__init__()
        self.orignal_image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.angle = math.radians(angle)
        self.damage = damage
        self.game = game
        self.velocity = pygame.Vector2(math.cos(self.angle) * speed, math.sin(self.angle) * speed)

    def update(self):
        # Move projectile
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Remove if off-screen
        if not self.game.screen.get_rect().colliderect(self.rect):
            self.kill()

    