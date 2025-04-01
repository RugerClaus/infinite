import pygame
from player import Player
from debug import DebugMenu
from button import Button
from enemy import Enemy
from item import Item

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
        self.music_manager = music_manager
        self.player = Player(50, 84, self.screen, self,music_manager)
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Enemy(800,700,self,self.player,'snail'))

        self.items = pygame.sprite.Group()
        self.items.add(Item(400,700,5,50,'baton',self))
        self.debug = DebugMenu(self.screen,self.window,self)
        self.background_x = 0 
        self.background_speed = 3
        self.background_scrolling = False
        self.enemy_jumped = False
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
        for item in self.items:
            self.screen.blit(item.image, (item.original_x + self.background_x, item.rect.y))

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
                self.items.update()
                self.items.draw(self.screen)
                self.player.update(self.items)
                self.player.draw()
                self.enemies.update()
                self.enemies.draw(self.screen)


                enemy_hit = pygame.sprite.spritecollideany(self.player, self.enemies)
                if enemy_hit:
                    self.player.health -= 1
                    for enemy in self.enemies: self.enemies.remove(enemy)
                    print(self.player.health)
                else:
                    for enemy in self.enemies:
                        if self.player.rect.bottom < enemy.rect.top:
                            self.enemy_jumped = True
                    if self.enemy_jumped and self.player.on_ground:
                        self.score += 1
                        self.enemy_jumped = False

                self.render_score()
            
            if self.debug.on:
                self.debug.update()

            pygame.display.flip()
            self.clock.tick(60)