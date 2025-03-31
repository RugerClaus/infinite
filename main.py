import pygame
import random
from sys import exit as ex

# Window class
class Window():
    def __init__(self, width, height):
        pygame.init()
        pygame.font.init()
        self.width = width
        self.height = height
        self.version = "Alpha 0.0.0.0.9"
        self.title = f"Into the SpaceHole Version {self.version}"
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.debug_font = pygame.font.Font('font/Pixeltype.ttf',25)
        self.button_font = pygame.font.Font('font/Roboto-Black.ttf', 30)
        self.button_fontgame_over_font = pygame.font.Font('font/gameover.ttf', 50)
        self.game_active = False
        self.window_state = 'main_menu'
        self.music_manager = SoundManager()
    
    def render_main_menu(self):
        self.window_state = 'main_menu'
        button_unhovered_color = "orange"
        button_hovered_color = "white"

        title = pygame.image.load("graphics/spacehole_title.png")
        title_rect = title.get_rect(center = (500,100))

        play_button = Button("Play!", 500, 192, 125, 50, self.button_font, button_unhovered_color, button_hovered_color,
                             self.start_game)
        options_button = Button("Options", 500, 384, 125, 50, self.button_font, button_unhovered_color,
                                button_hovered_color, self.render_options_menu)
        quit_button = Button("Exit", 500, 576, 125, 50, self.button_font, button_unhovered_color, button_hovered_color,
                             self.quit_game)

        self.screen.fill((255, 128, 0))
        self.screen.blit(title,title_rect)
        play_button.draw(self.screen, pygame.mouse.get_pos())
        options_button.draw(self.screen, pygame.mouse.get_pos())
        quit_button.draw(self.screen, pygame.mouse.get_pos())

        pygame.display.flip()

        self.handle_ui_events([play_button, options_button, quit_button])

    def render_options_menu(self):
        self.window_state = 'options_menu'
        button_unhovered_color = "orange"
        button_hovered_color = "white"

        # buttons
        self.music_toggle_button = Button(f"Music: {self.music_manager.music_status()}", 500, 200, 150, 50, self.button_font, button_unhovered_color, button_hovered_color, self.toggle_music)
        self.sfx_toggle_button = Button(f"SFX: {self.music_manager.sfx_status()}", 500, 400, 150, 50, self.button_font, button_unhovered_color, button_hovered_color, self.toggle_sfx)
        back_button = Button("Back", 500, 600, 100, 50, self.button_font, button_unhovered_color, button_hovered_color, self.render_main_menu)

        self.screen.fill((255, 128, 0))
        self.music_toggle_button.draw(self.screen,pygame.mouse.get_pos())
        self.sfx_toggle_button.draw(self.screen,pygame.mouse.get_pos())
        back_button.draw(self.screen, pygame.mouse.get_pos())

        pygame.display.flip()

        self.handle_ui_events([back_button,self.music_toggle_button,self.sfx_toggle_button])

    def toggle_music(self):
        self.music_manager.toggle_music('menu')
        self.music_toggle_button.text = f"Music: {self.music_manager.music_status()}"
    
    def toggle_sfx(self):
        self.music_manager.toggle_sfx()
        self.sfx_toggle_button.text = f"SFX: {self.music_manager.sfx_status()}"

    def handle_ui_events(self, buttons):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        button.is_clicked(pygame.mouse.get_pos(), event.button == 1)
                elif event.type == pygame.MOUSEMOTION:
                    return

    def start_game(self):
        self.music_manager.stop_music()
        self.window_state = 'in_game'
        game = Game(True,self.screen,self.clock,self,self.music_manager)
        game.game_loop()

    def quit_game(self):
        print("Goodbye!")
        pygame.quit()
        ex()

    def main_loop(self):
        while self.running:

            if self.window_state == "main_menu":
                self.render_main_menu()
                self.music_manager.play_music('menu')
            elif self.window_state == 'options_menu':
                self.render_options_menu()
            elif self.window_state == "in_game":
                self.start_game()

            self.clock.tick(30)

class SoundManager:
    def __init__(self, volume=0.5):
        pygame.mixer.init()
        self.music_tracks = {
            "menu": "audio/menu_music.wav",
            "game": "audio/game_music.wav"
        }
        self.sound_effects = {
            "jump": 'audio/jump.mp3'
        }
        self.volume = volume
        self.music_active = True
        self.sfx_active = True

    def play_music(self, track_name, loop=True):
        if not self.music_active:
            return
        if track_name in self.music_tracks:
            if pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() > 0:
                return
            pygame.mixer.music.load(self.music_tracks[track_name])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1 if loop else 0)

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_track = None

    def toggle_music(self,state):

        if self.music_active:
            pygame.mixer.music.stop()
            print("Music off")
            self.current_track = None
        else:
            if state in self.music_tracks:
                pygame.mixer.music.load(self.music_tracks[state])
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.current_track = state
                print(f"Music on: {state}")

        self.music_active = not self.music_active

    def set_volume(self, volume):
        self.volume = max(0, min(volume, 1))  # Ensure volume is between 0 and 1
        pygame.mixer.music.set_volume(self.volume)

    def play_sfx(self, sfx_name):
        if self.sfx_active and sfx_name in self.sound_effects:
            sfx = pygame.mixer.Sound(self.sound_effects[sfx_name])
            sfx.set_volume(self.volume)
            sfx.play()

    def stop_sfx(self):
        pygame.mixer.stop()


    def toggle_sfx(self):
        self.sfx_active = not self.sfx_active
        print(f"SFX {'On' if self.sfx_active else 'Off'}")

    
    def sfx_status(self):
        return "On" if self.sfx_active else "Off"

    def music_status(self):
        if self.music_active == True:
            return "On"
        else:
            return "Off"


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

class Button():
    def __init__(self, text, x, y, width, height, font, text_unhovered_color, text_hovered_color, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.action = action
        self.text_unhovered_color = text_unhovered_color
        self.text_hovered_color = text_hovered_color
        self.color = "black"

        self.surface = pygame.Surface((self.width, self.height))
        self.text_surface = self.font.render(self.text, True, self.text_unhovered_color)
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            text_color = self.text_hovered_color
        else:
            text_color = self.text_unhovered_color

        self.text_surface = self.font.render(self.text, True, text_color)

        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos) and mouse_click:
            if self.action:
                self.action()


class Animation:
    def __init__(self, frames, frame_delay):
        self.frames = frames
        self.frame_delay = frame_delay
        self.current_frame = 0
        self.frame_timer = 0

    def update(self):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_current_frame(self):
        return self.frames[self.current_frame]

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, game):
        super().__init__()
        self.x = x
        self.walking = False
        self.y = y
        self.speed = 0
        self.gravity = 0
        self.jumping = False
        self.max_jump_height = 200
        self.rect = pygame.rect.Rect(x,y,64,84)
        self.screen = screen
        self.on_ground = True
        self.game = game
        self.walking_left = False
        self.was_walking = self.walking

        #going right
        self.walking_frames = [
            pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha(),
            pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        ]
        self.walking_animation = Animation(self.walking_frames,10)
        self.jumping_frame = [pygame.image.load("graphics/Player/jump.png").convert_alpha()]
        self.jumping_animation = Animation(self.jumping_frame,10)

        #going left
        self.walking_backward_frames = [
            pygame.image.load("graphics/Player/player_walk_back_1.png").convert_alpha(),
            pygame.image.load("graphics/Player/player_walk_back_2.png").convert_alpha()
        ]
        self.walking_backward_animation = Animation(self.walking_backward_frames,10)
        self.jumping_back_frame = [pygame.image.load("graphics/Player/jump_back.png").convert_alpha()]
        self.jumping_backward_animation = Animation(self.jumping_back_frame,10)

        #facing forward
        self.holding_still_frame = [pygame.image.load("graphics/Player/player_stand.png").convert_alpha()]
        self.holding_still_animation = Animation(self.holding_still_frame,10)
        


    def update(self):
        
        if not self.on_ground:
            self.gravity += 0.5  
            self.jumping_animation.update()

        if self.on_ground and not self.walking:
            self.holding_still_animation.update()

        if self.rect.bottom >= 701:
            self.rect.bottom = 700
            self.gravity = 0
            self.on_ground = True 

            if self.was_walking and self.speed != 0:
                self.walking = True

        if self.walking and self.on_ground:
            if self.speed > 0: #right
                self.walking_animation.update()
            elif self.speed < 0: #left
                self.walking_backward_animation.update()

        if self.rect.left < self.screen.get_width() // 2:
            
            self.rect.x += self.speed
        elif self.rect.left >= self.screen.get_width() // 2:
            
            if self.game.background_x == 0:
                
                self.rect.x += self.speed
            elif self.game.background_x == -2900:
                
                self.rect.x += self.speed
            else:
                self.rect.x = self.screen.get_width() // 2
        if self.rect.x <= 0 or self.rect.x >= 1000 and self.game.background_x <= -3100:
            self.speed = 0

        
        self.rect.y += self.gravity
        

    def jump(self):
        if self.on_ground:
            self.gravity = -15
            self.on_ground = False
            self.was_walking = self.walking
            self.walking = False
            print("Jumping!")

    def draw(self):
        if not self.on_ground:
            self.walking = False
            if self.speed > 0: #right
                self.image = self.jumping_animation.get_current_frame()
            elif self.speed < 0: #left
                self.image = self.jumping_backward_animation.get_current_frame()
        elif self.walking:
            if self.speed > 0: #right
                self.image = self.walking_animation.get_current_frame()
            elif self.speed < 0: #left
                self.image = self.walking_backward_animation.get_current_frame()
        else:
            self.image = self.holding_still_frame[0]
        self.screen.blit(self.image, self.rect)


class Game():
    def __init__(self, game_active, screen, clock, window,music_manager):
        self.paused = False
        self.game_active = game_active
        self.pause_button_font = pygame.font.Font('font/Pixeltype.ttf', 40)
        self.score_font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.score = 0
        self.clock = clock
        self.window = window
        self.screen = screen
        self.player = Player(50, 700, self.screen, self)
        self.debug = DebugMenu(self.screen,self.window,self)
        self.background_x = 0 
        self.background_speed = 3
        self.background_scrolling = False
        self.music_manager = music_manager
        self.check_state()

    def check_state(self):
        if self.game_active:
            self.game_loop()
        else:
            self.window.render_main_menu()

    def exit(self):
        self.window.quit_game()

    def reset(self):
        self.score = 0
        self.player.reset()

    def render_score(self):
        score_surface = self.score_font.render(f'Score: {self.score}', True, (64, 64, 64))
        self.screen.blit(score_surface, (866, 5))

    def render_pause_menu(self):
        self.paused = True
        resume_button = Button("Resume", 100, 75, 100, 50, self.pause_button_font, (173, 216, 230), (255, 255, 255), self.update_pause_state)
        self.music_toggle_button = Button(f"Music: {self.music_manager.music_status()}",100,150,125,50,self.pause_button_font,(173,216,230),(255,255,255),self.toggle_music)
        self.sfx_toggle_button = Button(f"SFX: {self.music_manager.sfx_status()}", 100, 225, 125, 50, self.pause_button_font,(173,216,230),(255,255,255), self.toggle_sfx)
        quittomenu_button = Button("Menu", 100, 300, 100, 50, self.pause_button_font, (173, 216, 230), (255, 255, 255), self.go_to_main_menu)
        quittodesktop_button = Button("Exit", 100, 375, 100, 50, self.pause_button_font, (173, 216, 230), (255, 255, 255), self.exit)
        
        buttons = [resume_button,self.music_toggle_button,self.sfx_toggle_button, quittomenu_button, quittodesktop_button]

        for button in buttons:
            button.draw(self.screen, pygame.mouse.get_pos())

        pygame.display.flip()

        return buttons
    
    def toggle_sfx(self):
        self.music_manager.toggle_sfx()
        self.sfx_toggle_button.text = f"SFX: {self.music_manager.sfx_status()}"

    def toggle_music(self):
        self.music_manager.toggle_music('game')
        self.music_toggle_button.text = f"Music: {self.music_manager.music_status()}"

    def go_to_main_menu(self):
        self.music_manager.stop_music()
        self.paused = False
        self.game_active = False
        self.window.window_state = 'main_menu'

    def update_pause_state(self):
        self.paused = not self.paused

    def update_background_position(self):
        if self.player.rect.centerx >= 500:
            self.background_scrolling = True
        elif self.background_x == 0:
            self.background_scrolling = False

        if self.background_scrolling:
            if self.player.speed > 0:
                self.background_x -= self.background_speed
            elif self.player.speed < 0:
                if self.background_x < 0:
                    self.background_x += self.background_speed

        if self.background_x <= -3000:
            self.background_scrolling = False
            self.player.rect.x += self.player.speed

    def render_environment(self):
        self.update_background_position()

        sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()

        self.screen.blit(sky_surface, (self.background_x, 400))
        self.screen.blit(sky_surface, (self.background_x + self.screen.get_width(), 400))

        ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

        self.screen.blit(ground_surface, (self.background_x, 700))

    def handle_player_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.player.speed = 5
                    self.player.walking = True
                elif event.key == pygame.K_a:
                    self.player.speed = -5  
                    self.player.walking = True
                elif event.key == pygame.K_SPACE:  
                    self.player.jump()
                    self.music_manager.play_sfx('jump')
                elif event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                #debug
                elif event.key == pygame.K_F2:
                    print(f"Background left x position: {self.background_x}")
                    print(f"player center x position: {self.player.rect.x}")
                elif event.key == pygame.K_F9:
                    if not self.debug.on:
                        self.debug.start()
                    else:
                        self.debug.stop()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    self.player.speed = 0
                    self.player.was_walking = self.player.walking
                    self.player.walking = False

    def game_loop(self):
        while self.game_active:
            if self.music_manager.music_status() == "On":
                self.music_manager.play_music('game')
            else:
                self.music_manager.stop_music()
            if self.paused:
                pause_buttons = self.render_pause_menu()
                while self.paused:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in pause_buttons:
                        button.draw(self.screen, mouse_pos)
                    pygame.display.flip()
                    self.window.handle_ui_events(pause_buttons)
            else:
                self.screen.fill((208, 244, 247))
                self.render_environment()
                self.handle_player_input()
                self.player.update()
                self.player.draw()
                self.render_score()
            
            if self.debug.on:
                self.debug.update()

            pygame.display.flip()
            self.clock.tick(60)

window = Window(1000, 800)
window.main_loop()
