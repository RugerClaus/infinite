import pygame

class Inventory():
    def __init__(self):
        self.x = 0
        self.y = 50
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
                self.render_column(column, self.x + (i + 1) * 50, screen)  # Render the inventory below the hotbar

    def render_column(self, start_slot, column_x, screen):
        current_slot = start_slot
        slot_y = self.y

        while current_slot:
            # Render the slot
            pygame.draw.rect(screen, (255, 255, 255), (column_x, slot_y, current_slot.size, current_slot.size))  # Slot size

            # Highlight the selected slot (for hotbar)
            if current_slot.index == self.selected_hotbar_slot:
                pygame.draw.rect(screen, (255, 0, 0), (column_x, slot_y, current_slot.size, current_slot.size), 3)  # Red border for selected slot
            else:
                pygame.draw.rect(screen, (0, 0, 0), (column_x, slot_y, current_slot.size, current_slot.size), current_slot.border)  # Default black border

            # Render item in the slot if present
            if current_slot.item:
                scaled_item_image = pygame.transform.scale(current_slot.item.image, (self.contained_item_max_width, self.contained_item_max_height))
                screen.blit(scaled_item_image, (column_x + 5, slot_y + 5))  # Render the scaled item in the slot

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
            current_slot = current_slot.right_slot  # Move to the next hotbar slot

        # If the selected hotbar slot is full, try to add the item to the inventory
        for row in self.inventory:
            current_slot = row
            while current_slot:
                if current_slot.item is None:  # If the slot is empty
                    current_slot.item = item  # Add the item to the slot
                    print(f"Item added to inventory slot with index {current_slot.index}")
                    return  # Exit after adding the item
                current_slot = current_slot.right_slot  # Move to the next slot

        print("Inventory is full. Could not add item.")  # If no empty slot is found

    def get_hotbar_slot_by_index(self, index):
        current_slot = self.hotbar
        while current_slot:
            if current_slot.index == index:
                return current_slot
            current_slot = current_slot.right_slot
        return None  # If no slot found

class Slot():
    def __init__(self, index):
        self.size = 48
        self.border = 2
        self.left_slot = None
        self.right_slot = None
        self.item = None
        self.index = index
