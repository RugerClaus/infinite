import pygame

class DebugMenu():
    def __init__(self,screen,window,game):
        self.on = False
        self.surface = pygame.surface.Surface((250,100))
        self.rect = self.surface.get_rect(bottomleft = (750,100))
        self.win = window
        self.game = game
        self.screen = screen
        self.fps_text = self.win.debug_font.render(f"FPS: {self.game.clock.get_fps()}",True,'white')
        self.version_text = self.win.debug_font.render(f"Ver: {self.win.version}",True,'white')
        

    def draw(self):
        self.surface.fill('lightblue')
        self.surface.blit(self.version_text,(20,15))
        self.surface.blit(self.fps_text, (20, 60))
        self.surface.blit(self.coords_text, (20, 75))
        self.surface.blit(self.nearest_enemy_text,(20,30))
        self.surface.blit(self.enemy_relation_to_player_text,(20,45))
        self.screen.blit(self.surface, self.rect)

    def start(self):
        print("Debug: On")
        self.on = True

    def stop(self):
        print("Debug: Off")
        self.on = False
    
    def update(self,nearest_enemy_data):
        if self.on:
            player_coords = (self.game.player.world_y, self.game.player.world_y)
            debug_x = self.game.player.rect.x + abs(self.game.world.background_x)
            if nearest_enemy_data:
                enemy_positon = nearest_enemy_data["position"]
                distance_x = enemy_positon[0] - self.game.player.rect.centerx
                distance_y = (enemy_positon[1]) - self.game.player.rect.bottom
                self.nearest_enemy_text = self.win.debug_font.render(
                    f"Nearest E dist: {(distance_x,distance_y)}", True, 'white'
                )
                self.enemy_relation_to_player_text = self.win.debug_font.render(
                    f"Dir to E: {nearest_enemy_data['relation_to_player']}",True,'white')
            elif nearest_enemy_data == None:
                self.nearest_enemy_text = self.win.debug_font.render(
                    "Nearest E dist: N/A", True, 'white'
                )
            self.fps_text = self.win.debug_font.render(f"FPS: {self.game.clock.get_fps()}", True, 'white')     
            self.coords_text = self.win.debug_font.render(f"Coordinates: ({debug_x},{player_coords[1]})", True, 'white')
            self.draw()