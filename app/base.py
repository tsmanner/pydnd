from collections import defaultdict
from random import randint

from typing import Iterable, Optional, Union

from .bonus import AttackBonus, Bonus, SaveBonus


class DndBase:
    def __init__(self, character):
        self.character = character
        self.attack = AttackBonus()
        self.save = SaveBonus(self)

    def __format__(self, format_spec):
        return str(self).__format__(format_spec)

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return Bonus()


class Die:
    def __init__(self, sides: int):
        self.sides = sides

    @property
    def roll(self):
        return randint(0, self.sides) + 1

    def __add__(self, other):
        if isinstance(other, int):
            return other + self.roll

    def __radd__(self, other):
        if isinstance(other, int):
            return other + self.roll

    def __lt__(self, other: "Die"):
        return self.sides < other.sides

    def __eq__(self, other: "Die"):
        return self.sides == other.sides

    def __str__(self):
        return f"d{self.sides}"


class Roll(list):
    def __init__(self, iterable: Optional[Iterable[Union[int, Die]]] = None):
        super().__init__()
        if iterable is not None:
            [self.append(item) for item in iterable]

    def append(self, item: Die):
        if not (isinstance(item, int) or isinstance(item, Die)):
            raise TypeError(f"unsupported type for Roll.append: '{item.__class__.__name__}'")
        super().append(item)

    def insert(self, index: int, item: Die):
        if not (isinstance(item, int) or isinstance(item, Die)):
            raise TypeError(f"unsupported type for Roll.insert: '{item.__class__.__name__}'")
        super().insert(index, item)

    @property
    def roll(self):
        return sum(self)

    def __setitem__(self, key: int, value: Die):
        if not (isinstance(value, int) or isinstance(value, Die)):
            raise TypeError(f"unsupported type for Roll.insert: '{value.__class__.__name__}'")
        super().__setitem__(key, value)

    def __str__(self):
        base = 0
        d_counts = defaultdict(int)
        for item in self:  # type: Die
            if isinstance(item, int):
                base += item
            else:
                d_counts[item.sides] += 1
        return "+".join([f"{base}"] + [f"{d_counts[k]}d{k}" for k in d_counts])
