from .base import DndBase
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
    def __init__(self, character):
        super().__init__(character)
        self.armor_class.append(1, "size")
        self.attack[""].append(1, "size")
        self.hide.append(4, "size")
        self.speed.append(20, "size")

    def carrying_capacity(self):
        return {
            "light": floor(self.character.abilities.strength * Race.LIGHT_LOAD * 3/4),
            "medium": floor(self.character.abilities.strength * Race.MEDIUM_LOAD * 3/4),
            "heavy": floor(self.character.abilities.strength * Race.HEAVY_LOAD * 3/4),
        }


class Medium(Race):
    def __init__(self, character):
        super().__init__(character)

    def carrying_capacity(self):
        return {
            "light": floor(self.character.abilities.strength * Race.LIGHT_LOAD),
            "medium": floor(self.character.abilities.strength * Race.MEDIUM_LOAD),
            "heavy": floor(self.character.abilities.strength * Race.HEAVY_LOAD),
        }


class Halfling(Small):
    def __init__(self, character):
        super().__init__(character)
        self.attack["sling"].append(1, "racial")
        self.attack["thrown"].append(1, "racial")
        self.climb.append(2, "racial")
        self.jump.append(2, "racial")
        self.move_silently.append(2, "racial")
        self.save["all"].append(1, "racial")
        self.save["fear"].append(2, "morale")
        self.character.abilities["racial"].strength -= 2
        self.character.abilities["racial"].dexterity += 2


class Human(Medium):
    def __init__(self, character):
        super().__init__(character)

