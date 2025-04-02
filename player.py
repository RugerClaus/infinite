import pygame
from math import sqrt
from animate import Animation
from entity import Entity

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
            self.walking = True  # Continue walking after landing if it was happening before

    def draw(self):
        super().draw()

    def get_nearest_enemy(self, enemies):
        nearest_enemy = None
        min_distance = float("inf")
        relation_to_player = ["", ""]

        for enemy in enemies:
            distance = sqrt((self.rect.centerx - enemy.rect.centerx) ** 2 + (self.rect.bottom - enemy.rect.bottom) ** 2)
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
