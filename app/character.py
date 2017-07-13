from .base import *
from .classes import *
from .feats import *
from .races import *
from typing import Dict, Optional, Type


class ClassProgression(list):
    def __init__(self):
        super().__init__()

    def class_level(self, dnd_class: Type[DndClass], character_level: Optional[int] = None):
        if character_level is None:
            return len(list(filter(lambda dc: isinstance(dc, dnd_class), self)))
        return len(list(filter(lambda dc: isinstance(dc, dnd_class), self[:character_level])))

    def append(self, dnd_class: Type[DndClass]):
        super().append(dnd_class(self.class_level(dnd_class) + 1))

    def __setitem__(self, key: int, dnd_class: Type[DndClass]):
        """ Replace a character level with a different class.
        1) Decrement the level of all subsequent instances of the old class
        2) Insert the new class instance
        3) Increment the level of all subsequent instances of the new class
        """
        old_type = type(super()[key])
        for item in self[key+1:]:
            if isinstance(item, old_type):
                item.level -= 1
        super().__setitem__(key, dnd_class(self.class_level(dnd_class, key + 1) + 1))
        for item in self[key+1:]:
            if isinstance(item, dnd_class):
                item.level += 1

    def insert(self, index: int, dnd_class: Type[DndClass]):
        super().insert(index, dnd_class(self.class_level(dnd_class, index + 1) + 1))
        for item in self[index+1:]:
            if isinstance(item, dnd_class):
                item.level += 1

    def current(self, character_level: Optional[int] = None):
        cur = {}
        if character_level is None:
            segment = self
        else:
            segment = self[:character_level]
        for cls in segment:
            cur[cls.__class__.__name__] = cls
        return list(cur.values())

    def __str__(self):
        return "\n".join([f"  Lvl BaB Fort Ref Will Class"] +
                         [f"  {i+1:>2}: "
                          f"{dcls.base_attack_bonus:^3} "
                          f"{dcls.fortitude_save:^4} "
                          f"{dcls.reflex_save:^3} "
                          f"{dcls.will_save:^4} "
                          f"{dcls}"
                          for i, dcls in enumerate(self)])


class Character:
    def __init__(self, race: Type[Race]):
        self.classes = ClassProgression()
        self.race = race()
        self.feats = {}  # type: Dict[int, Feat]
        self.flaws = {}  # type: Dict[int, Flaw]

    def level_up(self, dnd_class: Type[DndClass]):
        self.classes.append(dnd_class)

    @property
    def level(self):
        return len(self.classes)

    def _aspects(self, level: Optional[int] = None):
        return self.classes.current(level) + [self.race]

    def base_attack_bonus(self, level: Optional[int] = None):
        return sum([item.attack["base"] for item in self._aspects(level)])

    def fortitude_save(self, level: Optional[int] = None):
        return sum([item.save["fortitude"] for item in self._aspects(level)])

    def reflex_save(self, level: Optional[int] = None):
        return sum([item.save["reflex"] for item in self._aspects(level)])

    def will_save(self, level: Optional[int] = None):
        return sum([item.save["will"] for item in self._aspects(level)])

    def __str__(self):
        lines = [f"Level {self.level} {self.race} [{', '.join([str(c) for c in self.classes.current()])}]"]
        if self.level == 0:
            return lines[0]
        lines.append("  Lvl BaB Fort Ref Will Class")
        for lvl in range(1, self.level+1):
            lines.append(f"  {lvl:>2}: "
                         f"{self.base_attack_bonus(lvl):^3} "
                         f"{self.fortitude_save(lvl):^4} "
                         f"{self.reflex_save(lvl):^3} "
                         f"{self.will_save(lvl):^4} "
                         f"{self.classes[lvl-1]}"
                         )
        return "\n".join(lines)
