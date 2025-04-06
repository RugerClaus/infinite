import pygame
from entities.player import Player
from UI.debug import DebugMenu
from UI.button import Button
from entities.enemy import *
from entities.weapon import *
from UI.ui import UI
from core.world import World
from core.cutscene import Cutscene
from core.state import *

class Game():
    def __init__(self, game_active, screen, clock, window,music_manager):
        self.paused = False
        self.state = State()
        self.game_active = game_active
        self.pause_button_font = pygame.font.Font('font/Pixeltype.ttf', 40)
        self.clock = clock
        self.window = window
        self.screen = screen
        self.music_manager = music_manager
        self.world = World(self)
        self.player = Player(self.screen, self,music_manager)
        self.enemies = pygame.sprite.Group()
        self.ui = UI(self)
        self.debug = DebugMenu(self.screen,self.window,self)
        self.cutscene = Cutscene(self)
        self.cutscene_played = False
        self.intro_music_playing = False
        self.game_music_playing = False
        



        ###### ADD ITEMS TO GAME - NEED TO AUTOMATE THIS#####
        self.projectiles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.items.add(LaserRifle(self))
        self.items.add(RedLaserRifle(self))
        self.items.add(Magnum(self))
        self.enemies.add(Snail(self,self.player))
        self.enemy_jumped = False

    def exit(self):
        self.window.quit_game()

    def reset(self):
        self.score = 0
        self.player.reset()

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
        self.state.set_state(APPSTATE.MAIN_MENU)

    def update_pause_state(self):
        self.paused = not self.paused

    def render_environment(self):
        self.world.update()
        self.world.render()

    # def handle_item_collection(self):
    #     # Check if the player collides with any item
    #     item_hit = pygame.sprite.spritecollideany(self.player, self.items)

    def handle_item_collection(self):
        # Check if the player collides with any item
        item_hit = pygame.sprite.spritecollideany(self.player, self.items)
        
        if item_hit:  # If there is a collision with an item
            if self.player.inventory["primary"] is None or self.player.inventory["secondary"] is None:  # Allow picking up if there is space
                self.ui.show_prompt(f"Press E to pick up {item_hit.canonical_name}:", item_hit.image, False)
            else:  # If inventory is full
                self.ui.show_prompt(f"Press E to swap {self.player.active_weapon.canonical_name} for {item_hit.name}", item_hit.image, True)

        if item_hit and pygame.key.get_pressed()[pygame.K_e]:  # If 'E' is pressed and an item is hit
            if self.player.inventory["primary"] is None:  # Check if there's space in the primary slot
                self.player.inventory['primary'] = item_hit  # Add item to inventory
                self.player.active_weapon = item_hit  # Set as active weapon
                self.items.remove(item_hit)  # Remove item from the world
                self.ui.show_prompt(f"Picked up {item_hit.name}!", item_hit.image, False)  # Update prompt

            elif self.player.inventory["secondary"] is None:  # If inventory is full
                self.player.inventory["secondary"] = item_hit  # Add item to inventory
                self.player.active_weapon = item_hit  # Set as active weapon
                self.items.remove(item_hit)  # Remove item from the world
                self.ui.show_prompt(f"Picked up {item_hit.name}!", item_hit.image, False)  # Update prompt
                
            else:  # If both inventory slots are full, swap items
                if isinstance(item_hit, Weapon):  # Only swap if the item is a weapon
                    current_weapon = self.player.inventory["primary"] if self.player.active_weapon == self.player.inventory["primary"] else self.player.inventory["secondary"]
                    
                    if current_weapon == self.player.inventory["primary"]:
                        self.player.inventory["primary"] = item_hit
                    else:
                        self.player.inventory["secondary"] = item_hit

                    self.player.active_weapon = item_hit  # Set new item as active weapon
                    item_hit.collected = True

                    # Remove the current weapon from the world and place it on the ground
                    if current_weapon in self.items:  # Ensure the current weapon is in the world before removing
                        current_weapon.collected = False
                        self.items.remove(current_weapon)
                        
                    if current_weapon not in self.items:
                        self.items.add(current_weapon)  # Add it back to the items group to be rendered on the ground

                    # Update the UI prompt
                    self.ui.show_prompt(f"Swapped {current_weapon.canonical_name} for {item_hit.name}", item_hit.image, True)
            self.music_manager.play_sfx(self.player.active_weapon.pickup_sound)


    def render_hotbar(self):
        hotbar_x, hotbar_y = 10, 0
        weapon_offset_x = 60 
        weapons = [self.player.inventory["primary"], self.player.inventory["secondary"]]

        for index, weapon in enumerate(weapons):
            if weapon:
                weapon_x = hotbar_x + index * weapon_offset_x
                weapon_rect = weapon.image_right.get_rect(topleft=(weapon_x, hotbar_y))
                self.screen.blit(weapon.image_left, weapon_rect)

                if self.player.active_weapon == weapon:
                    pygame.draw.rect(self.screen, (0, 0, 0), weapon_rect, 5)  # Highlight active weapon
            else:
                placeholder_image = pygame.Surface((50, 50))
                placeholder_image.fill((169, 169, 169))  # Gray placeholder for empty slots
                self.screen.blit(placeholder_image, (hotbar_x + index * weapon_offset_x, hotbar_y))


    def handle_player_input(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.window.quit_game()
            if event.type == pygame.MOUSEWHEEL:
                self.player.switch_weapons()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pass
                #print(f"Key Pressed: {event.key}, Setting Selected Index to: {self.hotbar.selected_index}")
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
                elif event.key == pygame.K_e:
                    pass
                elif event.key == pygame.K_F2:
                    pass
                elif event.key == pygame.K_F3:
                    pass
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.player.attack()
    def game_loop(self):
        while self.game_active:
            if self.music_manager.music_status() == "On":
                if not self.cutscene_played:
                    if not self.intro_music_playing:
                        self.music_manager.play_music('intro')
                        self.intro_music_playing = True
                        self.game_music_playing = False  # reset in case we go back
                else:
                    if not self.game_music_playing:
                        self.music_manager.stop_music()
                        self.music_manager.play_music('game')
                        self.game_music_playing = True
                        self.intro_music_playing = False
            else:
                self.music_manager.stop_music()
                self.intro_music_playing = False
                self.game_music_playing = False
            if self.paused:
                pause_buttons = self.render_pause_menu()
                while self.paused:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in pause_buttons:
                        button.draw(self.screen, mouse_pos)
                    pygame.display.flip()
                    self.window.handle_ui_events(pause_buttons)
            if not self.cutscene_played:
                self.cutscene.play_cutscene()
            else:
                self.screen.fill((208, 244, 247))
                if self.debug.on:
                    self.debug.update(nearest_enemy_data)
                self.render_environment()
                self.handle_player_input()
                self.items.update()
                self.items.draw(self.screen)
                self.player.update()
                self.player.draw()
                self.enemies.update()
                self.enemies.draw(self.screen)
                
                self.handle_item_collection()
                self.render_hotbar()
                self.projectiles.update()
                self.projectiles.draw(self.screen)
                nearest_enemy_data = self.player.get_nearest_enemy(self.enemies)

                if self.debug.on:
                    self.debug.update(nearest_enemy_data)
                
                # if not any(enemy.type == 'snail' for enemy in self.enemies):
                #     new_snail = Enemy(900, 700, self, self.player, 'snail')
                #     self.enemies.add(new_snail)
                



            pygame.display.flip()
            self.clock.tick(60)