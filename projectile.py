import pygame
import math
from entity import Entity

class Projectile(Entity):
    def __init__(self,x,y,angle,speed,damage,image,game):
        super().__init__(game.screen)
        self.original_image = image
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center= (x,y))
        self.speed = speed
        self.angle = math.radians(angle)
        self.damage = damage
        self.game = game
        self.velocity = pygame.Vector2(math.cos(self.angle) * speed, math.sin(self.angle) * speed)

    def update(self):
        # Move projectile
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        # print(f"Projectile position: {self.x,self.y}")
        # Remove if off-screen
        if not self.game.screen.get_rect().colliderect(self.rect) or self.rect.bottom >= 700:
            self.kill()
        for enemy in self.game.enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.health -= self.damage
                self.kill()
                print(enemy.health)
                