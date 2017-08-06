__all__ = [
    "DndClass",
    "MasterThrower",
    "Ninja",
    "Wizard",
]

import math
from .base import Die, DndBase


class DndClass(DndBase):
    def __init__(self, character, level, hit_die):
        super().__init__()
        self.character = character
        self.level = level
        self.hit_die = Die(hit_die)
        self.hit_points = self.hit_die.roll
        self.fortitude.append(self.save_secondary(), "class")
        self.reflex.append(self.save_secondary(), "class")
        self.will.append(self.save_secondary(), "class")

    def __str__(self):
        return f"{self.__class__.__name__}{self.level}"

    """
    Utility functions
        Base Attack Bonus Progressions
            bab_1: +1 per level
            bab_0_75: +3 per 4 levels (0.75/lvl)
            bab_0_5: +1 per 2 levels (0.5/lvl)
        Saving Throw Progressions
            save_primary: 2 +1 per 2 levels (2 + 0.5/lvl)
            save_secondary: 0 +1 per 3 levels (0.33/lvl
    """

    def bab_1(self):
        return self.level

    def bab_0_75(self):
        return math.floor((3/4) * self.level)

    def bab_0_5(self):
        return math.floor((1/2) * self.level)

    def save_primary(self):
        return 2 + math.floor((1/2) * self.level)

    def save_secondary(self):
        return math.floor((1/3) * self.level)


class PresigeClass(DndClass):
    def __init__(self, character, level, hit_die, prerequisites = None):
        super().__init__(character, level, hit_die)



"""
Class Definitions
"""


class Ninja(DndClass):
    """ Ninja (Complete Adventurer)
    Base Attack Bonus: 0.75/lvl
    Fortitude Save: Secondary (0.33/lvl)
    Reflex Save: Secondary (0.33/lvl)
    Will Save: Primary (2 + 0.5/lvl)
    """
    def __init__(self, character, level):
        super().__init__(character, level, 6)
        # TODO: How to easily add this as part of the level based bonuses.
        # TODO:   Refactor everything so a "Player" has a "Character" list which shows increments?
        # TODO:   Let AC etc be "global" and print them as part of the header?
        self.character.armor_class.append(int(character.bonus("wisdom")) + (level // 5), "ninja")
        self.attack["base"].append(self.bab_0_75(), "class")
        self.will[0] = (self.save_primary(), "class")


class Wizard(DndClass):
    """ Wizard (Player's Handbook, Core Rulebook I)
    Base Attack Bonus: 0.5/lvl
    Fortitude Save: Secondary (0.33/lvl)
    Reflex Save: Secondary (0.33/lvl)
    Will Save: Primary (2 + 0.5/lvl)
    """
    def __init__(self, character, level):
        super().__init__(character, level, 4)
        self.attack["base"].append(self.bab_0_5(), "class")
        self.will[0] = (self.save_primary(), "class")


class MasterThrower(PresigeClass):
    """ Master Thrower (Complete Warrior)
    Base Attack Bonus: 1/lvl
    Fortitude Save: Secondary (0.33/lvl)
    Reflex Save: Primary (2 + 0.5/lvl)
    Will Save: Secondary (0.33/lvl)
    """
    def __init__(self, character, level):
        super().__init__(character, level, 8)
        self.attack["base"].append(self.bab_0_5(), "class")
        self.reflex[0] = (self.save_primary(), "class")
