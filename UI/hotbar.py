import pygame

class Hotbar():
    def __init__(self,screen,inventory,window):
        self.screen = screen
        self.inventory = inventory

        self.slot_size = 50
        self.padding = 3
        self.selected_padding = 15
        self.number_of_slots = 6

        self.width = self.number_of_slots * (self.slot_size + self.padding) - self.padding
        self.x = 950
        self.y = 50
        self.selected_index = 0
        self.color = (255,255,255)

    def draw(self):
        hotbar_surface = pygame.Surface((self.width, self.number_of_slots * (self.slot_size + self.padding)), pygame.SRCALPHA)
        hotbar_surface.set_alpha(150)

        for i in range(self.number_of_slots):
            slot_x = self.x
            slot_y = self.y + i * (self.slot_size + self.padding)

            pygame.draw.rect(self.screen, self.color, (slot_x, slot_y, self.slot_size, self.slot_size), border_radius=5)
            pygame.draw.rect(self.screen, (0, 0, 0), (slot_x, slot_y, self.slot_size, self.slot_size), 2)

            slot_color = (128, 128, 128) if i == self.selected_index else (255, 255, 255)
            pygame.draw.rect(self.screen, slot_color, (slot_x, slot_y, self.slot_size, self.slot_size), border_radius=5) #updates this again so that I can control the inventory slots.

            if i < len(self.inventory.items):  
                item = self.inventory.items[i]
                
                if item.image:
                    item_width, item_height = item.image.get_size()

                    if item_height >= self.slot_size:
                        item_height -= 10
                    if item_width >= self.slot_size:
                        item_width -= 10
                    scaled_image = pygame.transform.scale(item.image, (item_width, item_height))

                    # Center the image in the slot
                    image_rect = scaled_image.get_rect(center=(slot_x + self.slot_size // 2, slot_y + self.slot_size // 2))
                    self.screen.blit(scaled_image, image_rect.topleft)
                else:
                    pygame.draw.rect(self.screen, (255, 255, 0), (slot_x, slot_y, self.slot_size, self.slot_size))  # Yellow box for missing images
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(item.name, True, (0, 0, 0))
                    self.screen.blit(text_surface, (slot_x + 5, slot_y + 5))

        self.screen.blit(hotbar_surface, (self.x, self.y))

    def update(self):
        self.hotbar_items = self.inventory.items[:self.number_of_slots]