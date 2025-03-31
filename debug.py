import pygame

class DebugMenu():
    def __init__(self,screen,window,game):
        self.on = False
        self.surface = pygame.surface.Surface((250,100))
        self.rect = self.surface.get_rect()
        self.win = window
        self.game = game
        self.screen = screen
        self.fps_text = self.win.debug_font.render(f"FPS: {self.game.clock.get_fps()}",True,'white')
        self.version_text = self.win.debug_font.render(f"Ver: {self.win.version}",True,'white')

    def draw(self):
        self.surface.fill('lightblue')
        self.surface.blit(self.version_text,(20,15))
        self.surface.blit(self.fps_text, (20, 45))
        self.surface.blit(self.coords_text, (20, 60))
        self.screen.blit(self.surface, self.rect)

    def start(self):
        print("Debug: On")
        self.on = True

    def stop(self):
        print("Debug: Off")
        self.on = False
    
    def update(self):
        if self.on:
            player_coords = (self.game.player.rect.x, self.game.player.rect.y)
            debug_x = self.game.player.rect.x + abs(self.game.background_x)
            self.fps_text = self.win.debug_font.render(f"FPS: {self.game.clock.get_fps()}", True, 'white')     
            self.coords_text = self.win.debug_font.render(f"Coordinates: ({debug_x},{player_coords[1]})", True, 'white')
            self.draw()