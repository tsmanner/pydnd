SMALL = 0
MEDIUM = 1
LARGE = 2


class Race:
    def __init__(self, name, size):
        self.size = size
        self.name = name

    def __str__(self):
        return self.name


class StrongheartHalfling(Race):
    def __init__(self):
        Race.__init__(self, "Strongheart Halfling", SMALL)


class Goblin(Race):
    def __init__(self):
        Race.__init__(self, "Goblin", SMALL)


races = {"Strongheart Halfling": StrongheartHalfling,
         "Goblin": Goblin}
