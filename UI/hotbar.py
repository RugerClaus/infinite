import pygame
class Hotbar():
    def __init__(self, game):
        self.game = game
        self.number_of_slots = 6  # Fixed number of slots.
        self.items = [None] * self.number_of_slots  # None means empty slot.
        self.selected_index = 0  # First item by default.

    def draw(self):
        # Simplified drawing: Just draw rectangles for each slot.
        for i in range(self.number_of_slots):
            slot_x = 0
            slot_y = 100 + i * 51

            if i == self.selected_index:
                border_color = (255,128,64)
                border_thickness = 4
            else:
                border_color = (255,255,255)
                border_thickness = 2

            pygame.draw.rect(self.game.screen,border_color, (slot_x, slot_y, 50, 50), border_thickness)  # Slot border.
            if self.items[i]:  # If there's an item in this slot.
                item_width, item_height = self.items[i].image.get_size()

                if item_height >= 50:
                    item_height -= 10
                if item_width >= 50:
                    item_width -= 10


                scaled_image = pygame.transform.scale(self.items[i].image, (item_width, item_height))
                pygame.draw.rect(self.game.screen, (255, 255, 255,100), (slot_x, slot_y, 50, 50), 2)
                self.game.screen.blit(scaled_image, (slot_x, slot_y))  # Draw item image

    def handle_input(self, mouse_pos):
        for i in range(self.number_of_slots):
            slot_x = 100 + i * 60
            slot_y = 50
            if slot_x <= mouse_pos[0] <= slot_x + 50 and slot_y <= mouse_pos[1] <= slot_y + 50:
                if pygame.mouse.get_pressed()[0]:  # Left click
                    self.selected_index = i
                    item = self.items[i]
                    if item:
                        # Move item from hotbar to inventory.
                        self.game.player.inventory.add_item(item)
                        self.items[i] = None  # Clear hotbar slot.
                    return
