from .base import BonusAtom, DndBase
from math import floor


class Race(DndBase):
    LIGHT_LOAD = 10/3
    MEDIUM_LOAD = 20/3
    HEAVY_LOAD = 30/3

    def __str__(self):
        return f"{self.__class__.__name__}"


class Small(Race):
    """
    +1 Armor Class
    +1 Attack Bonus
    +4 Hide
    ~2/3 Speed (20)
    3/4 Carry Capacity
    """
    def __init__(self):
        super().__init__()
        self.armor_class.append(1, "size")
        self.attack[""].append(1, "size")
        self.hide.append(4, "size")
        self.speed.append(20, "size")

    @staticmethod
    def carrying_capacity(strength: int):
        return {
            "light": floor(strength * Race.LIGHT_LOAD * 3/4),
            "medium": floor(strength * Race.MEDIUM_LOAD * 3/4),
            "heavy": floor(strength * Race.HEAVY_LOAD * 3/4),
        }


class Medium(Race):
    def __init__(self):
        super().__init__()

    @staticmethod
    def carrying_capacity(strength: int):
        return {
            "light": floor(strength * Race.LIGHT_LOAD),
            "medium": floor(strength * Race.MEDIUM_LOAD),
            "heavy": floor(strength * Race.HEAVY_LOAD),
        }


class Halfling(Small):
    def __init__(self):
        super().__init__()
        self.attack["sling"].append(1, "racial")
        self.attack["thrown"].append(1, "racial")
        self.climb.append(2, "racial")
        self.dexterity.append(2, "racial")
        self.jump.append(2, "racial")
        self.move_silently.append(2, "racial")
        self.save["all"].append(1, "racial")
        self.save["fear"].append(2, "morale")
        self.strength.append(-2, "racial")


class Human(Medium):
    def __init__(self):
        super().__init__()

