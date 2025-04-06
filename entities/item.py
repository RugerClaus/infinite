import pygame
from entities.animate import Animation
from entities.entity import Entity

class Item(Entity):
    def __init__(self, game, x, y, name, item_class, scrolls_with_background=False):
        super().__init__(game.screen, False, 0)
        self.game = game
        self.name = name
        self.world_x = x
        self.world_y = y
        self.world = self.game.world
        self.original_x = x
        self.item_class = item_class
        self.is_in_hotbar = False
        self.scrolls_with_background = scrolls_with_background
        self.collected = False
        self.rect = None
        
        self.image = self.load_image()

        if self.image is None:
            print(f"Error: Failed to load image for item {self.name}!")
        else:
            self.rect = self.image.get_rect(bottomleft=(self.world_x, self.world_y))
            self.set_animation("idle", Animation([self.image], 10))

    def load_image(self):
        image_path = f"graphics/Items/{self.item_class}/{self.name}_left.png"
        try:
            return pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading image from {image_path}: {e}")
            return None

    def update(self):
        super().update()
        if not self.collected:
            offset_x = self.world.background_x if self.scrolls_with_background else 0
            self.rect.x = self.world_x + offset_x
            self.rect.y = self.world_y
        else:
            self.collected = False
            self.kill()
