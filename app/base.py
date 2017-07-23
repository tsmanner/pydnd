from collections import defaultdict
from random import randint
from typing import Iterable, Optional, Union


class BonusAtom(int):
    stacking_sources = [
        "class",
        "dodge",
    ]

    def __new__(cls, value, source: str, *args):
        new_bonus = int.__new__(cls, value, *args)
        new_bonus.source = source
        return new_bonus


class Bonus(list):
    @property
    def sources(self):
        return {item.source for item in self}

    """ Arithmetic Methods """

    def __add__(self, other):
        if isinstance(other, int):
            return int(self) + other
        elif isinstance(other, Bonus):
            return Bonus(super().__add__(other))
        raise TypeError(f"unsupported operand type(s) for +: "
                        f"'{self.__class__.__name__}' and '{other.__class__.__name__}'")

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, int):
            return int(self) * other
        raise TypeError(f"unsupported operand type(s) for *: "
                        f"'{self.__class__.__name__}' and '{other.__class__.__name__}'")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            return int(self) - other
        raise TypeError(f"unsupported operand type(s) for -: "
                        f"'{self.__class__.__name__}' and '{other.__class__.__name__}'")

    def __rsub__(self, other):
        return other - int(self)

    """ Access Methods """

    def append(self, item: Union[BonusAtom, int], source: Optional[str] = None):
        if isinstance(item, int) and isinstance(source, str):
            item = BonusAtom(item, source)
        if not isinstance(item, BonusAtom):
            raise TypeError(f"Bonus.append expects BonusAtom objects, actual: {item.__class__.__name__}")
        super().append(item)

    def insert(self, index: int, item: Union[BonusAtom, int], source: Optional[str] = None):
        if isinstance(item, int) and isinstance(source, str):
            item = BonusAtom(item, source)
        if not isinstance(item, BonusAtom):
            raise TypeError(f"Bonus.insert expects BonusAtom objects, actual: {item.__class__.__name__}")
        super().insert(index, item)

    def extend(self, iterable: Iterable[BonusAtom]):
        for item in iterable:
            self.append(item)

    def __getitem__(self, item):
        if isinstance(item, str):
            return filter(lambda b: b.source == item, self)
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        if isinstance(value, tuple) and len(value) == 2 and isinstance(value[0], int) and isinstance(value[1], str):
            value = BonusAtom(*value)
        super().__setitem__(key, value)

    """ Conversion Methods """

    def __int__(self):
        bonuses = []
        for source in self.sources:
            if source in BonusAtom.stacking_sources:
                bonuses.extend(self[source])
            else:
                bonuses.append(max(self[source]))
        return int(sum(bonuses))

    def __repr__(self):
        return "Bonus" + super().__repr__()

    def __str__(self):
        return str(int(self))


class BonusGroup(defaultdict):
    def __init__(self):
        super().__init__(Bonus)


class AttackBonus(BonusGroup):
    types = {

    }


class SaveBonus(BonusGroup):
    links = {
        "fear": "will",
        "fortitude": "constitution",
        "reflex": "dexterity",
        "will": "wisdom",
    }

    def __init__(self, parent: "DndBase"):
        super().__init__()
        self.parent = parent

    def __getitem__(self, item: str):
        save = super().__getitem__(item)
        if item in self.links:
            linked = self.links[item]
            if linked in self.parent.character.abilities.ability_names:
                print(self.parent.character.abilities[2])
                save += self.parent.character.abilities[2][linked]  # TODO: Figure out how to attach the level here.
            save += self[self.links[item]]
        if "all" in self:
            save += super().__getitem__("all")
        return save


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
