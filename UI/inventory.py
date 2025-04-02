import pygame
import time

class Inventory():
    def __init__(self,window):
        self.window = window
        self.x = 0
        self.y = 0
        self.contained_item_max_height = 40
        self.contained_item_max_width = 40
        self.hotbar = self.create_linked_list(5, 0)
        self.inventory = [
            self.create_linked_list(5, 5),
            self.create_linked_list(5, 10),
            self.create_linked_list(5, 15),
            self.create_linked_list(5, 20)
        ]
        self.open = False
        self.selected_hotbar_slot = 0
        self.last_selected_time = 0
        self.selection_fade_duration = 1.0

    def create_linked_list(self, num_slots, start_index):
        head = Slot(start_index)
        current_slot = head
        current_index = start_index

        for _ in range(1, num_slots):
            new_slot = Slot(current_index+1)
            current_slot.right_slot = new_slot
            new_slot.left_slot = current_slot
            current_slot = new_slot
            current_index += 1
        current_slot.right_slot = None
        return head

    def render(self, screen):
        # Render the hotbar and inventory vertically
        self.render_column(self.hotbar, self.x, screen)  # Render the hotbar as a column
        for i, column in enumerate(self.inventory):
            if self.open:
                self.render_column(column, self.x + (i + 1) * 65, screen)  # Render the inventory below the hotbar

    def render_column(self, start_slot, column_x, screen):
        current_slot = start_slot
        slot_y = self.y

        while current_slot:
            # Render the slot
            pygame.draw.rect(screen, (255, 255, 255), (column_x, slot_y, current_slot.size, current_slot.size))  # Slot size

            # Highlight the selected slot (for hotbar)
            if current_slot.index == self.selected_hotbar_slot:
                if current_slot.item is not None:
                    self.render_selected_item_name(screen,current_slot)
                pygame.draw.rect(screen, (255, 0, 0), (column_x, slot_y, current_slot.size, current_slot.size), 3)  # Red border for selected slot
            else:
                pygame.draw.rect(screen, (0, 0, 0), (column_x, slot_y, current_slot.size, current_slot.size), current_slot.border)  # Default black border

            # Render item in the slot if present
            if current_slot.item:
                original_width = current_slot.item.image.get_width()
                original_height = current_slot.item.image.get_height()

                # Maintain aspect ratio while fitting within max width and height
                scale_factor = min(self.contained_item_max_width / original_width, self.contained_item_max_height / original_height)
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                scaled_item_image = pygame.transform.scale(current_slot.item.image, (new_width, new_height))

                screen.blit(scaled_item_image, ((column_x+40) - current_slot.item.image.get_width(), slot_y+ 5))  # Render the scaled item in the slot
                if current_slot.item.is_stackable and current_slot.item.stack_size > 1:
                    screen.blit(self.window.inventory_font.render(f"{current_slot.item.stack_size}",True,'black'), (column_x + 4, slot_y + 38))

            # Move to the next slot
            if current_slot.right_slot:
                current_slot = current_slot.right_slot
                slot_y += current_slot.size + current_slot.border  # Update y position for the next slot
            else:
                break

    def toggle_inventory(self):
        self.open = not self.open

    def add_item(self, item):
        current_slot = self.hotbar
        while current_slot:
            if current_slot.item is None:  # If the slot is empty
                current_slot.item = item  # Add the item to the slot
                print(f"Item added to hotbar slot with index {current_slot.index}")
                return  # Stop after adding the item
            
            elif current_slot.item.is_stackable and isinstance(current_slot.item, type(item)):
                # If the item is stackable and is the same type, increase its stack count
                current_slot.item.stack_size += 1
                print(f"Stacked item in hotbar slot with index {current_slot.index}. New stack size: {current_slot.item.stack_size}")
                return

            current_slot = current_slot.right_slot  # Move to the next hotbar slot

        # If the selected hotbar slot is full, try to add the item to the inventory
        for column in self.inventory:
            current_slot = column
            while current_slot:
                if current_slot.item is None:  # If the slot is empty
                    current_slot.item = item  # Add the item to the slot
                    print(f"Item added to inventory slot with index {current_slot.index}")
                    return  # Exit after adding the item
                
                elif current_slot.item.is_stackable and isinstance(current_slot.item, type(item)):
                    # Stack items in inventory
                    current_slot.item.stack_size += 1
                    print(f"Stacked item in inventory slot with index {current_slot.index}. New stack size: {current_slot.item.stack_size}")
                    return
                
                current_slot = current_slot.right_slot  # Move to the next slot

        print("Inventory is full. Could not add item.")  # If no empty slot is found

    def get_hotbar_slot_by_index(self, index):
        current_slot = self.hotbar
        while current_slot:
            if current_slot.index == index:
                return current_slot
            current_slot = current_slot.right_slot
        return None  # If no slot found

    def select_hotbar_slot(self, index):
        self.selected_hotbar_slot = index
        self.last_selected_time = time.time()
        print(f"Selected hotbar slot: {index}, Time: {self.last_selected_time}")
    
    def render_selected_item_name(self, screen, current_slot):
        if not current_slot or not current_slot.item:
            return  # Don't render if no item is in the selected slot
        
        font = self.window.inventory_font
        current_time = time.time()
        time_elapsed = current_time - self.last_selected_time
        if time_elapsed < self.selection_fade_duration:
            text_surface = font.render(f"{current_slot.item.name}", True, 'black')
            screen.blit(text_surface, (70, 150))  # Position of the text

class Slot():
    def __init__(self, index):
        self.size = 60
        self.border = 2
        self.left_slot = None
        self.right_slot = None
        self.item = None
        self.index = index
