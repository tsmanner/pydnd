__all__ = [
    "Race",
    "Tiny",
    "Small",
    "Medium",
    "Halfling",
    "Human",
]

from .base import DndBase
from math import floor


class Race(DndBase):
    LIGHT_LOAD = 10/3
    MEDIUM_LOAD = 20/3
    HEAVY_LOAD = 30/3

    def __str__(self):
        return f"{self.__class__.__name__}"


class Tiny(Race):
    """
    +2 Armor Class
    +2 Attack Bonus
    +8 Hide
    -8 Grapple
    1/2 Carry Capacity
    """
    def __init__(self):
        super().__init__()
        self.armor_class.append(2, "size")
        self.attack[""].append(2, "size")
        self.attack["grapple"].append(-8, "size")
        self.hide.append(8, "size")

    def carrying_capacity(self):
        return {
            "light": floor(self.character.abilities.strength * Race.LIGHT_LOAD * 1/2),
            "medium": floor(self.character.abilities.strength * Race.MEDIUM_LOAD * 1/2),
            "heavy": floor(self.character.abilities.strength * Race.HEAVY_LOAD * 1/2),
        }


class Small(Race):
    """
    +1 Armor Class
    +1 Attack Bonus
    +4 Hide
    3/4 Carry Capacity
    """
    def __init__(self):
        super().__init__()
        self.armor_class.append(1, "size")
        self.attack[""].append(1, "size")
        self.attack["grapple"].append(-4, "size")
        self.hide.append(4, "size")

    def carrying_capacity(self):
        return {
            "light": floor(self.character.abilities.strength * Race.LIGHT_LOAD * 3/4),
            "medium": floor(self.character.abilities.strength * Race.MEDIUM_LOAD * 3/4),
            "heavy": floor(self.character.abilities.strength * Race.HEAVY_LOAD * 3/4),
        }


class Medium(Race):
    def __init__(self):
        super().__init__()

    def carrying_capacity(self):
        return {
            "light": floor(self.character.abilities.strength * Race.LIGHT_LOAD),
            "medium": floor(self.character.abilities.strength * Race.MEDIUM_LOAD),
            "heavy": floor(self.character.abilities.strength * Race.HEAVY_LOAD),
        }


class Halfling(Small):
    def __init__(self):
        super().__init__()
        self.attack["sling"].append(1, "racial")
        self.attack["thrown"].append(1, "racial")
        self.climb.append(2, "racial")
        self.jump.append(2, "racial")
        self.move_silently.append(2, "racial")
        self.fortitude.append(1, "racial")
        self.reflex.append(1, "racial")
        self.will.append(1, "racial")
        self.fear.append(2, "morale")
        self.strength.append(-2, "racial")
        self.dexterity.append(2, "racial")
        self.speed.append(20, "racial")


class Human(Medium):
    def __init__(self):
        super().__init__()

