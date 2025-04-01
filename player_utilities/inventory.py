class Inventory():
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"Picked up {item.name}")
    
    def drop_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Dropped {item.name}")

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            removed_item = self.items.pop(index)
            print(f"Dropped {removed_item.name}")
        else:
            print("Invalid index for remove_item.")

    def display_inventory(self):
        if self.items:
            print(f"Inventory: {[item.name for item in self.items]}")
        else:
            print("Inventory is empty")
