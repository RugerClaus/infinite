import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x,y,width,height,screen):
        super().__init__()
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        self.rect = pygame.Rect(x,y,width,height)
        
        self.screen = screen

    def update(self):
        self.world_y = self.rect.bottom - 700

    def draw(self):
        self.screen.blit(self.image,self.rect)