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
                border_color = (255, 128, 64)
                border_thickness = 4
            else:
                border_color = (255, 255, 255)
                border_thickness = 2

            pygame.draw.rect(self.game.screen, border_color, (slot_x, slot_y, 50, 50), border_thickness)  # Slot border.
            if self.items[i] and self.items[i].image:  # If there's an item in this slot.
                self.items[i].is_in_hotbar = True
                item_width, item_height = self.items[i].image.get_size()

                # Calculate new size while maintaining aspect ratio
                scale_factor = min(40 / item_width, 40 / item_height)
                new_width = int(item_width * scale_factor)
                new_height = int(item_height * scale_factor)

                # Resize image while keeping aspect ratio
                scaled_image = pygame.transform.scale(self.items[i].image, (new_width, new_height))

                # Center the item in the slot
                x_offset = slot_x + (50 - new_width) // 2 # Center in 50px wide slot
                y_offset = slot_y + (50 - new_height) // 2  # Center in 50px high slot

                self.game.screen.blit(scaled_image, (x_offset, y_offset))


    def handle_input(self, mouse_pos):
        if pygame.mouse.get_pressed()[0]:  # Left mouse button is held
            if not hasattr(self, 'last_click') or not self.last_click:  # Only trigger once per click
                for i in range(self.number_of_slots):
                    slot_x = 0
                    slot_y = 100 + i * 51

                    if slot_x <= mouse_pos[0] <= slot_x + 50 and slot_y <= mouse_pos[1] <= slot_y + 50:
                        self.selected_index = i
                        item = self.items[i]

                        if item:
                            if self.game.player.inventory.add_item(item):  # Only move if successful
                                print(f"Put {self.items[i].name} in inventory.")
                                self.items[i].is_in_hotbar = False
                                self.items[i] = None  # Remove item from hotbar
                                
                        self.last_click = True  # Prevents repeated calls
        else:
            self.last_click = False  # Reset when mouse is released