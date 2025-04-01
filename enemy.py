import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,game,player):
        super().__init__()

        self.x = x
        self.y = y
        self.game = game
        self.screen = game.screen
        self.music_manager = game.music_manager
        self.player = player

        self.image = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (x,y))
        self.speed = 3

    def update(self):

        if self.player:
            if self.rect.x > self.player.rect.x:
                self.rect.x -= self.speed
            else:
                self.rect.x -= self.speed

    def draw(self):
        self.screen.blit(self.image,self.rect)

