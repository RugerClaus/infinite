class Inventory():
    def __init__(self):
        self.items = []

    def add_item(self, item):
        if item not in self.items:  # Avoid duplicates
            self.items.append(item)  # Move, don't copy
            return True  # Indicate success
        return False  # Inventory full or item already present
            
    
    def drop_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Dropped {item.name}")

    def hotbar_item(self, index):
        if 0 <= index < len(self.items):
            hotbar_item = self.items.pop(index)
            hotbar_item.is_in_hotbar = True
            print(f"Put {hotbar_item.name} in hotbar")
        else:
            print("Invalid index for hotbar item.")

    def display_inventory(self):
        if self.items:
            print(f"Inventory: {[item.name for item in self.items]}")
        else:
            print("Inventory is empty")
