class Collision():

    def __init__(self,entities):
        self.entities = entities

        if type(self.entities) is not list:
            print("Entities should be a list")
            return
        else:
            for entity in self.entities:
                position = (entity.x,entity.y)