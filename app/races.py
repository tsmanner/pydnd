from .base import BonusAtom, DndBase


class Race(DndBase):
    def __str__(self):
        return f"{self.__class__.__name__}"


class Small(Race):
    def __init__(self):
        super().__init__()
        self.armor_class.append(1, "size")
        self.attack[""].append(1, "size")
        self.dexterity.append(2, "size")
        self.hide.append(4, "size")
        self.speed.append(20, "size")
        self.strength.append(-2, "size")


class Medium(Race):
    def __init__(self):
        super().__init__()


class Halfling(Small):
    def __init__(self):
        super().__init__()
        self.attack["sling"].append(1, "racial")
        self.attack["thrown"].append(1, "racial")
        self.climb.append(2, "racial")
        self.jump.append(2, "racial")
        self.move_silently.append(2, "racial")
        self.save["all"].append(1, "racial")
        self.save["fear"].append(2, "morale")


class Human(Medium):
    def __init__(self):
        super().__init__()

