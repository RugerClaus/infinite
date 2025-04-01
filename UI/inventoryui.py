import pygame

class InventoryUI():
    def __init__(self, game):
        self.game = game
        self.is_open = False
        self.slot_size = 50  # Size of each inventory slot
        self.columns = 4      # Number of columns in the inventory
        self.rows = 6        # Max rows (adjust as needed)
        self.padding = 5     # Space between slots

    def toggle_inventory(self):
        self.is_open = not self.is_open

    def draw(self):
        if self.is_open:
            for row in range(self.rows):
                for col in range(self.columns):
                    x = 200 + col * (self.slot_size + self.padding)
                    y = 150 + row * (self.slot_size + self.padding)
                    
                    # Draw slot border (for all slots, even empty ones)
                    pygame.draw.rect(self.game.screen, (255, 255, 255), (x, y, self.slot_size, self.slot_size), 2)
            
            # Now draw the actual items in the inventory
            for i, item in enumerate(self.game.player.inventory.items):
                col = i % self.columns
                row = i // self.columns
                x = 200 + col * (self.slot_size + self.padding)
                y = 150 + row * (self.slot_size + self.padding)

                if item and item.image:
                    item_width, item_height = item.image.get_size()

                    # Calculate new size while maintaining aspect ratio
                    scale_factor = min((self.slot_size - 10) / item_width, (self.slot_size - 10) / item_height)
                    new_width = int(item_width * scale_factor)
                    new_height = int(item_height * scale_factor)

                    # Resize image while keeping aspect ratio
                    scaled_image = pygame.transform.scale(item.image, (new_width, new_height))

                    # Center the item in the slot
                    x_offset = x + (self.slot_size - new_width) // 2
                    y_offset = y + (self.slot_size - new_height) // 2

                    self.game.screen.blit(scaled_image, (x_offset, y_offset))
    def handle_input(self, mouse_pos):
        if pygame.mouse.get_pressed()[0]:  # Left mouse button is held
            if not hasattr(self, 'last_click') or not self.last_click:  # Only trigger once per click
                for i, item in enumerate(self.game.player.inventory.items):
                    slot_x = 200 + (i % self.columns) * (self.slot_size + 10)
                    slot_y = 150 + (i // self.columns) * (self.slot_size + 10)

                    if slot_x <= mouse_pos[0] <= slot_x + 50 and slot_y <= mouse_pos[1] <= slot_y + 50:
                        # Check if the item is already in the hotbar (to avoid duplicates)
                        if item.is_in_hotbar:
                            print(f"{item.name} is already in the hotbar.")
                            return  # If the item is in the hotbar, do nothing
                        
                        # Loop through hotbar slots
                        for j in range(self.game.hotbar.number_of_slots):
                            if not self.game.hotbar.items[j]:  # If hotbar slot is empty
                                self.game.hotbar.items[j] = item  # Move item to hotbar
                                self.game.player.inventory.hotbar_item(i)  # Remove from inventory
                                item.is_in_hotbar = True  # Mark item as in hotbar
                                print(f"Moved {item.name} to hotbar.")
                                return  # Exit after moving the item

                self.last_click = True  # Prevents repeated calls
            else:
                self.last_click = False  # Reset when mouse is released