__all__ = [
    "Feat",
    "Flaw",
    "point_blank_shot",
    "precise_shot",
    "weapon_focus",
    "craven",
    "fiery_burst",
    "invisible_needle",
    "noncombatant",
    "vulnerable",
]

from functools import lru_cache
from typing import List, Optional, Union

from app.base import DndBase


class Feat(DndBase):
    def __init__(self, name: str, description: str,
                 prerequisites: Optional[List[Union[str, "Feat"]]] = None):
        super().__init__()
        self.name = name
        self.description = description
        self.prerequisites = prerequisites

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class Flaw(Feat):
    def __init__(self, name: str, description: str,
                 feat: Feat):
        super().__init__(name, description)
        self.feat = feat

    def __str__(self):
        return f"{self.name}({self.feat})"


"""
Feat Definitions
"""
point_blank_shot = Feat("Point Blank Shot", "+1 Attack Bonus and Damage with ranged weapons when within 30'")
precise_shot = Feat("Precise Shot", "No -4 Attack Bonus penalty for shooting into melee.", [point_blank_shot])
craven = Feat("Craven", "Add character level to sneak attack damage.")
fiery_burst = Feat("Fiery Burst", "Nd6 Fire ball, 5' radius, 30' range.", [])
invisible_needle = Feat("Invisible Needle", "Nd4 force darts as thrown weapons.", [])


@lru_cache()
def weapon_focus(weapon: str):
    feat = Feat(f"Weapon Focus({weapon})", "+1 Attack Bonus with {weapon}s")
    return feat

"""
Flaw Factories
"""


def noncombatant(feat: Feat):
    flaw = Flaw("Noncombatant", "-2 on melee Attack Bonus", feat)
    flaw.attack["melee"].append(-2, "flaw")
    return flaw


def vulnerable(feat: Feat):
    flaw = Flaw("Vulnerable", "-1 Armor Class", feat)
    flaw.armor_class.append(-1, "flaw")
    return flaw
