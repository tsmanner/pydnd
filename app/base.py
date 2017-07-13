from collections import defaultdict
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
    types = {
        "fear": "will",
    }

    def __getitem__(self, item: str):
        save = super().__getitem__(item)
        if item in self.types:
            save += self[self.types[item]]
        if "all" in self:
            save += super().__getitem__("all")
        return save


class DndBase:
    def __init__(self):
        self.attack = AttackBonus()
        self.save = SaveBonus()

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return Bonus()
