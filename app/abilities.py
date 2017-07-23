class Abilities:
    def __init__(self):
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0

    def __getitem__(self, item):
        return self.__getattribute__(item)
