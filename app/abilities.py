from collections import defaultdict
from functools import reduce
from typing import DefaultDict, Union


class Abilities:
    def __init__(self,
                 strength: int = 0,
                 dexterity: int = 0,
                 constitution: int = 0,
                 intelligence: int = 0,
                 wisom: int = 0,
                 charisma: int = 0
                 ):
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisom
        self.charisma = charisma

    def __add__(self, other: Union["Abilities", int]):
        if isinstance(other, Abilities):
            return Abilities(self.strength + other.strength,
                             self.dexterity + other.dexterity,
                             self.constitution + other.constitution,
                             self.intelligence + other.intelligence,
                             self.wisdom + other.wisdom,
                             self.charisma + other.charisma)
        elif isinstance(other, int) and int == 0:
            return Abilities(self.strength,
                             self.dexterity,
                             self.constitution,
                             self.intelligence,
                             self.wisdom,
                             self.charisma)
        raise TypeError(f"unsupported operand type(s) for +: "
                        f"'{self.__class__.__name__}' and '{other.__class__.__name__}'")

    def __radd__(self, other):
        return self.__add__(other)

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.__getattribute__(item)
        raise TypeError(f"attribute name '{item}' must be string, not '{item.__class__.__name__}'")


class AbilityProgression(defaultdict):  # type: DefaultDict[Union[str, int], Abilities]
    ability_names = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]

    def __init__(self):
        super().__init__(Abilities)

    def level(self, item: Union[str, int]):
        if not isinstance(item, int):
            raise TypeError(f"argument to {self.__class__.__name__}.AbilityProgression must be 'int'")
        abilities = Abilities()
        print([self[key] for key in filter(lambda k: isinstance(k, str) or k <= item, self)])
        return reduce(lambda a, b: a + b,
                      [self[key] for key in filter(lambda k: isinstance(k, str) or k <= item, self)],
                      abilities)
