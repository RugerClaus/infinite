import pygame
import math
from animate import Animation
from entity import Entity
from weapon import Weapon

class Player(Entity):
    def __init__(self, screen, game, music_manager):
        super().__init__(screen, has_gravity=True, health=10)
        self.game = game
        self.music_manager = music_manager
        self.speed = 0
        self.walking = False
        self.was_walking = False
        self.image = pygame.image.load(f"graphics/Player/player_stand.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = 700
        
        self.inventory = {"primary":None,"secondary":None}
        self.active_weapon = None

        # Animations
        self.set_animation("idle", Animation([pygame.image.load("graphics/Player/player_stand.png").convert_alpha()], 10))
        self.set_animation("walk_right", Animation([
            pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha(),
            pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        ], 10))
        self.set_animation("walk_left", Animation([
            pygame.image.load("graphics/Player/player_walk_back_1.png").convert_alpha(),
            pygame.image.load("graphics/Player/player_walk_back_2.png").convert_alpha()
        ], 10))
        self.set_animation("jump_right", Animation([pygame.image.load("graphics/Player/jump.png").convert_alpha()], 10))
        self.set_animation("jump_left", Animation([pygame.image.load("graphics/Player/jump_back.png").convert_alpha()], 10))

    def update(self, items_group):
        self.world_x = self.rect.centerx
        self.world_y = self.rect.bottom - 700
        super().update()

        # Handle animations
        if not self.on_ground:
            self.play_animation("jump_right" if self.speed >= 0 else "jump_left")
        elif self.walking:
            self.play_animation("walk_right" if self.speed > 0 else "walk_left")
        elif pygame.mouse.get_pos()[0] > self.rect.centerx:
            self.image = pygame.image.load(f"graphics/Player/player_walk_1.png")
        elif pygame.mouse.get_pos()[0] < self.rect.centerx:
            self.image = pygame.image.load(f"graphics/Player/player_walk_back_1.png")
        else:
            self.play_animation("idle")

        # Handle player movement & background scrolling
        if self.rect.left < self.screen.get_width() // 2 or self.game.background_x in [0, -2900]:
            self.rect.x += self.speed
        else:
            self.rect.x = self.screen.get_width() // 2

        # Prevent movement beyond boundaries
        if self.rect.x <= 0 or (self.rect.x >= 1000 and self.game.background_x <= -3100):
            self.speed = 0

    def jump(self):
        if self.on_ground:
            self.gravity = -15
            self.on_ground = False
            self.was_walking = self.walking
            self.music_manager.play_sfx('jump')
            print("Jumping!")

    def land(self):
        self.on_ground = True
        if self.was_walking:
            self.walking = True

    def draw(self):
        super().draw()
        if self.active_weapon:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.rect.centerx
            dy = mouse_y - self.rect.centery
            angle = math.degrees(math.atan2(dy, dx))

            facing_right = dx >= 0 and self.speed >= 0
            self.active_weapon.update_image(facing_right)

            weapon_offset_x = 20 if facing_right else -60
            weapon_offset_y = 0
            weapon_x = self.rect.centerx + weapon_offset_x
            weapon_y = self.rect.centery + weapon_offset_y
            if facing_right:
                rotated_weapon = pygame.transform.rotate(self.active_weapon.image, -angle)
            else:
                rotated_weapon = pygame.transform.rotate(self.active_weapon.image, -angle + 180)
            weapon_rect = rotated_weapon.get_rect(center=(weapon_x + 15, weapon_y + 15))
            self.screen.blit(rotated_weapon, weapon_rect.topleft)

    def switch_weapons(self):
        if self.inventory["primary"] and self.inventory["secondary"]:
            self.active_weapon = self.inventory["primary"] if self.active_weapon == self.inventory["secondary"] else self.inventory["secondary"]
            self.music_manager.play_sfx(self.active_weapon.pickup_sound)
            print(f"Switched to: {self.active_weapon.canonical_name}")

    def attack(self):
        if self.active_weapon:
            self.active_weapon.use()


    def get_nearest_enemy(self, enemies):
        nearest_enemy = None
        min_distance = float("inf")
        relation_to_player = ["", ""]

        for enemy in enemies:
            distance = math.sqrt((self.rect.centerx - enemy.rect.centerx) ** 2 + (self.rect.bottom - enemy.rect.bottom) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy

        if nearest_enemy:
            # Horizontal relation
            relation_to_player[0] = "Left" if nearest_enemy.rect.centerx < self.rect.centerx else "Right"

            # Vertical relation
            if nearest_enemy.rect.top < self.rect.bottom:
                relation_to_player[1] = "Up"
            elif nearest_enemy.rect.bottom > self.rect.top:
                relation_to_player[1] = "Down"
            else:
                relation_to_player[1] = "Level"

            return {
                "position": (nearest_enemy.rect.centerx, nearest_enemy.rect.midbottom[1]),
                "type": nearest_enemy.type,
                "relation_to_player": relation_to_player
            }
        
        return None