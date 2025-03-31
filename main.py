import pygame
import random
from sys import exit as ex

# Window class
class Window():
    def __init__(self, width, height, title="Juggernot 5k"):
        pygame.init()
        pygame.font.init()
        self.width = width
        self.height = height
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.debug_font = pygame.font.Font('font/Pixeltype.ttf',30)
        self.button_font = pygame.font.Font('font/Roboto-Black.ttf', 30)
        self.button_fontgame_over_font = pygame.font.Font('font/gameover.ttf', 50)

        self.music_active = False
        self.sfx_active = False
        self.game_active = False
        self.window_state = 'main_menu'

    def render_main_menu(self):
        self.window_state = 'main_menu'
        button_unhovered_color = "orange"
        button_hovered_color = "white"

        play_button = Button("Play!", 500, 192, 125, 50, self.button_font, button_unhovered_color, button_hovered_color,
                             self.start_game)
        options_button = Button("Options", 500, 384, 125, 50, self.button_font, button_unhovered_color,
                                button_hovered_color, self.render_options_menu)
        quit_button = Button("Exit", 500, 576, 125, 50, self.button_font, button_unhovered_color, button_hovered_color,
                             self.quit_game)

        self.screen.fill((255, 128, 0))
        play_button.draw(self.screen, pygame.mouse.get_pos())
        options_button.draw(self.screen, pygame.mouse.get_pos())
        quit_button.draw(self.screen, pygame.mouse.get_pos())

        pygame.display.flip()

        # Event loop for menu screen
        self.handle_ui_events([play_button, options_button, quit_button])

    def render_options_menu(self):
        self.window_state = 'options_menu'
        button_unhovered_color = "orange"
        button_hovered_color = "white"

        # buttons
        back_button = Button("Back", 400, 300, 100, 50, self.button_font, button_unhovered_color, button_hovered_color,
                             self.render_main_menu)

        self.screen.fill((255, 128, 0))
        back_button.draw(self.screen, pygame.mouse.get_pos())

        pygame.display.flip()

        self.handle_ui_events([back_button])

    def handle_ui_events(self, buttons):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        button.is_clicked(pygame.mouse.get_pos(), event.button == 1)
                elif event.type == pygame.MOUSEMOTION:  # Ensure buttons update on hover
                    return  # Break the loop and refresh the buttons

    def start_game(self):
        self.window_state = 'in_game'
        game = Game(True, self.screen, self.clock, self)
        game.game_loop()

    def quit_game(self):
        print("Goodbye!")
        pygame.quit()
        ex()

    def toggle_music(self):
        if self.music_active == True:
            self.music_active == False
        else:
            self.music_active = True

    def toggle_sfx(self):
        if self.sfx_active == True:
            self.sfx_active = False
        else:
            self.sfx_active = True

    def main_loop(self):
        while self.running:

            if self.window_state == "main_menu":
                self.render_main_menu()
            elif self.window_state == 'options_menu':
                self.render_options_menu()
            elif self.window_state == "in_game":
                self.start_game()

            self.clock.tick(30)

class DebugMenu():
    def __init__(self,screen,window,game):
        self.on = False
        self.surface = pygame.surface.Surface((250,75))
        self.rect = self.surface.get_rect()
        self.win = window
        self.game = game
        self.screen = screen
        self.fps_text = self.win.debug_font.render(f"FPS: {self.game.clock.get_fps()}",True,'white')

    def draw(self):
        self.surface.fill('lightblue')
        self.surface.blit(self.fps_text, (20, 20))
        self.surface.blit(self.coords_text, (20, 50))
        self.screen.blit(self.surface, self.rect)

    def start(self):
        self.on = True

    def stop(self):
        self.on = False
    
    def update(self):
        if self.on:
            player_coords = (self.game.player.rect.x, self.game.player.rect.y)
            debug_x = self.game.player.rect.x + abs(self.game.background_x)
            self.fps_text = self.win.debug_font.render(f"FPS: {self.game.clock.get_fps()}", True, 'white')     
            self.coords_text = self.win.debug_font.render(f"Player(x, y): ({debug_x},{player_coords[1]})", True, 'white')
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
            text_color = self.text_hovered_color  # Use hovered color when mouse is over
        else:
            text_color = self.text_unhovered_color  # Use unhovered color otherwise

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
        self.max_jump_height = 200  # Maximum height of the jump
        self.rect = pygame.rect.Rect(x,y,64,84)
        self.screen = screen
        self.on_ground = True  # Track whether the player is on the ground or in the air
        self.game = game  # Reference to the game object to access the background position
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
    def __init__(self, game_active, screen, clock, window):
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

        # Background scrolling parameters
        self.background_x = 0  # Position of first background
        self.background_speed = 3  # Adjusted Background speed for smoother scrolling
        self.background_scrolling = False  # Start with background not scrolling
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
        quittomenu_button = Button("Menu", 100, 150, 100, 50, self.pause_button_font, (173, 216, 230), (255, 255, 255), self.go_to_main_menu)
        quittodesktop_button = Button("Exit", 100, 220, 100, 50, self.pause_button_font, (173, 216, 230), (255, 255, 255), self.exit)
        
        buttons = [resume_button, quittomenu_button, quittodesktop_button]

        for button in buttons:
            button.draw(self.screen, pygame.mouse.get_pos())

        pygame.display.flip()

        return buttons

    def go_to_main_menu(self):
        self.paused = False
        self.game_active = False
        self.window.window_state = 'main_menu'

    def update_pause_state(self):
        self.paused = not self.paused

    def update_background_position(self):
        # Start scrolling the background only after the player reaches x = 500
        if self.player.rect.centerx >= 500:
            self.background_scrolling = True  # Enable scrolling
        elif self.background_x == 0:
            self.background_scrolling = False

        if self.background_scrolling:
            if self.player.speed > 0:  # Player moving right
                self.background_x -= self.background_speed
            elif self.player.speed < 0:  # Player moving left
                # Stop scrolling once background reaches (0, 0)
                if self.background_x < 0:
                    self.background_x += self.background_speed

        # Reset the background to create a seamless scroll effect
        if self.background_x <= -3000:
            self.background_scrolling = False# replace this with level complete logic
            self.player.rect.x += self.player.speed

    def render_environment(self):
        self.update_background_position()  # Update background position based on player speed

        # Sky
        sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()

        # Blit the two backgrounds
        self.screen.blit(sky_surface, (self.background_x, 400))
        self.screen.blit(sky_surface, (self.background_x + self.screen.get_width(), 400))

        # Ground
        ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

        # Blit the two ground images
        self.screen.blit(ground_surface, (self.background_x, 700))

    def handle_player_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:  # Move right
                    self.player.speed = 5  # Increase speed for smoother movement
                    self.player.walking = True
                elif event.key == pygame.K_a:  # Move left
                    self.player.speed = -5  
                    self.player.walking = True
                elif event.key == pygame.K_SPACE:  
                    self.player.jump()
                elif event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                #debug
                elif event.key == pygame.K_F2:
                    print(f"Background left x position: {self.background_x}")
                    print(f"player center x position: {self.player.rect.x}")
                elif event.key == pygame.K_F9:
                    if not self.debug.on:  # Toggle debug only when it's off
                        self.debug.start()
                    else:  # If it's on, turn it off
                        self.debug.stop()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    self.player.speed = 0  # Stop movement when key is released
                    self.player.was_walking = self.player.walking
                    self.player.walking = False

    def game_loop(self):
        while self.game_active:
            if self.paused:
                pause_buttons = self.render_pause_menu()
                while self.paused:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in pause_buttons:
                        button.draw(self.screen, mouse_pos)
                    pygame.display.flip()
                    self.window.handle_ui_events(pause_buttons)
            else:
                self.screen.fill((208, 244, 247))  # Set a background color (optional)
                self.render_environment()  # Render the moving background
                self.handle_player_input()
                self.player.update()
                self.player.draw()
                self.render_score()
            
            if self.debug.on:
                self.debug.update()

            pygame.display.flip()
            self.clock.tick(60)

window = Window(1000, 800, "Into the SpaceHole Version Alpha 0.0.0.0.8")
window.main_loop()
