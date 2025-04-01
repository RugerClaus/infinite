class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self,item):
        self.items.append(item)
        print(f"Picked up {item.name}")
    
    def drop_item(self,item):
        if item in self.items:
            self.items.remove(item)
            print(f"Dropped {item.name}")

    def display_inventory(self):
        if self.items:
            print(f"Inventory: {[item.name for item in self.items]}")
        else:
            print("Inventory is empty, you cuck")