__all__ = [
    "DndClass",
    "MasterThrower",
    "Ninja",
    "Wizard",
]

import math
from app.base import Die, DndBase

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


def bab_1(level):
    return level


def bab_0_75(level):
    return math.floor((3/4) * level)


def bab_0_5(level):
    return math.floor((1/2) * level)


def save_primary(level):
    return 2 + math.floor((1/2) * level)


def save_secondary(level):
    return math.floor((1/3) * level)


"""
DndBase
    DndClass
        Ninja
        Wizard
    PrestigeClass
        MasterThrower
"""


class DndClass(DndBase):
    def __init__(self, character, level, hit_die):
        super().__init__()
        self.character = character
        self.level = level
        self.hit_die = Die(hit_die)
        self.hit_points = self.hit_die.roll()
        self.fortitude.append(save_secondary(level), "class")
        self.reflex.append(save_secondary(level), "class")
        self.will.append(save_secondary(level), "class")

    def __str__(self):
        return f"{self.__class__.__name__}{self.level}"


class PrestigeClass(DndClass):
    def __init__(self, character, level, hit_die, prerequisites=None):
        super().__init__(character, level, hit_die)
        self.prerequisites = prerequisites


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
        self.attack["base"].append(bab_0_75(level), "class")
        self.will[0] = (save_primary(level), "class")


class Wizard(DndClass):
    """ Wizard (Player's Handbook, Core Rulebook I)
    Base Attack Bonus: 0.5/lvl
    Fortitude Save: Secondary (0.33/lvl)
    Reflex Save: Secondary (0.33/lvl)
    Will Save: Primary (2 + 0.5/lvl)
    """
    def __init__(self, character, level):
        super().__init__(character, level, 4)
        self.attack["base"].append(bab_0_5(level), "class")
        self.will[0] = (save_primary(level), "class")


class MasterThrower(PrestigeClass):
    """ Master Thrower (Complete Warrior)
    Base Attack Bonus: 1/lvl
    Fortitude Save: Secondary (0.33/lvl)
    Reflex Save: Primary (2 + 0.5/lvl)
    Will Save: Secondary (0.33/lvl)
    """
    def __init__(self, character, level):
        super().__init__(character, level, 8)
        self.attack["base"].append(bab_0_5(level), "class")
        self.reflex[0] = (save_primary(level), "class")
