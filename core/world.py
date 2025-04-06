import pygame


class World:
    def __init__(self, game):
        self.game = game  # Gives access to screen, player, etc.
        self.background_x = 0
        self.background_speed = 3
        self.background_scrolling = False

        self.level_bg = pygame.image.load('graphics/World/world_1/background.png').convert_alpha()
        self.level_ground = pygame.image.load('graphics/World/world_1/ground.jpg').convert_alpha()
        self.ground_rect = self.level_ground.get_rect()

    def update(self):
        player = self.game.player

        # Background scrolling logic
        if player.rect.centerx >= 500:
            self.background_scrolling = True
        elif self.background_x == 0:
            self.background_scrolling = False

        if self.background_scrolling:
            if player.speed > 0:
                self.background_x -= self.background_speed
            elif player.speed < 0 and self.background_x < 0:
                self.background_x += self.background_speed

        # Clamp scrolling to world bounds
        if self.background_x <= -3000:
            self.background_scrolling = False
            player.rect.x += player.speed

    def render(self):
        screen = self.game.screen

        # Sky
        screen.blit(self.level_bg, (self.background_x, 0))

        # Ground
        screen.blit(self.level_ground, (self.background_x, 700))