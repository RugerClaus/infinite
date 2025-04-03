import pygame
from sound import SoundManager
from UI.button import Button
from game import Game
from sys import exit as ex


class Window():
    def __init__(self, width, height):
        pygame.init()
        pygame.font.init()
        self.width = width
        self.height = height
        self.version = "Alpha 0.0.0.1.65"
        self.title = f"Into the SpaceHole Version {self.version}"
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.inventory_font = pygame.font.Font('font/Pixeltype.ttf',45)
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

        title = pygame.image.load("graphics/spacehole_title.png").convert_alpha()
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
        volume_down_button = Button(f"-",450,300,50,50,self.button_font,button_unhovered_color,button_hovered_color, self.music_volume_down)
        level_placeholder = Button(f"{round(int(self.music_manager.volume*10), 1)}",500,300,50,50,self.button_font,button_unhovered_color,button_unhovered_color,None)
        volume_up_button = Button(f"+",550,300,50,50,self.button_font,button_unhovered_color,button_hovered_color, self.music_volume_up)
        self.sfx_toggle_button = Button(f"SFX: {self.music_manager.sfx_status()}", 500, 400, 150, 50, self.button_font, button_unhovered_color, button_hovered_color, self.toggle_sfx)
        back_button = Button("Back", 500, 600, 100, 50, self.button_font, button_unhovered_color, button_hovered_color, self.render_main_menu)

        if not self.music_manager.music_active:
            level_placeholder.text = "/"
            volume_down_button.text = ""
            volume_up_button.text = ""
            volume_down_button.action = None
            volume_up_button.action = None

        self.screen.fill((255, 128, 0))
        self.music_toggle_button.draw(self.screen,pygame.mouse.get_pos())
        volume_down_button.draw(self.screen,pygame.mouse.get_pos())
        volume_up_button.draw(self.screen,pygame.mouse.get_pos())
        level_placeholder.draw(self.screen,pygame.mouse.get_pos())
        self.sfx_toggle_button.draw(self.screen,pygame.mouse.get_pos())
        back_button.draw(self.screen, pygame.mouse.get_pos())

        buttons = [back_button,self.music_toggle_button,volume_down_button,volume_up_button,self.sfx_toggle_button]

        pygame.display.flip()


        self.handle_ui_events(buttons)


    def music_volume_down(self):
        self.music_manager.set_volume(self.music_manager.volume - 0.1)

    def music_volume_up(self):
        self.music_manager.set_volume(self.music_manager.volume + 0.1)

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

            self.clock.tick(60)