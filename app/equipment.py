__all__ = [
    "Equipment",
    "cloak_of_resistance",
    "gloves_of_dexterity",
    "periapt_of_wisdom",
    "ring_of_ua_reduce_person_1_str",
]

from functools import lru_cache
from app.base import DndBase


class Equipment(DndBase):
    def __init__(self, name: str, price: int):
        super().__init__()
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}"


@lru_cache()
def cloak_of_resistance(n: int):
    assert 1 <= n <= 4
    cloak = Equipment(f"Cloak of Resistance +{n}", 1000 * (n**2))
    cloak.fortitude.append(n, "enhancement")
    cloak.reflex.append(n, "enhancement")
    cloak.will.append(n, "enhancement")
    return cloak


@lru_cache()
def gloves_of_dexterity(n: int):
    assert 1 <= n <= 4
    gloves = Equipment(f"Gloves of Dexterity +{n}", 1000 * (n**2))
    gloves.dexterity.append(n, "enhancement")
    return gloves


@lru_cache()
def periapt_of_wisdom(n: int):
    assert 1 <= n <= 4
    periapt = Equipment(f"Periapt of Wisdom +{n}", 1000 * (n**2))
    periapt.wisdom.append(n, "enhancement")
    return periapt

ring_of_ua_reduce_person_1_str = Equipment("Ring of Use Activated Reduce Person and +1 Strength", 5500)
ring_of_ua_reduce_person_1_str.strength.append(1, "enhancement")
