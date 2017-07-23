from .abilities import AbilityProgression
from .base import *
from .classes import *
from .feats import *
from .races import *
from typing import Dict, Optional, Type


class ClassProgression(list):
    def __init__(self, character):
        super().__init__()
        self.character = character

    def _update_hit_points(self):
        if len(self) > 0:
            self[0].hit_points = self[0].hit_die.sides
        for dcls in self[1:]:  # type: DndClass
            dcls.hit_points = dcls.hit_die.roll

    def class_level(self, dnd_class: Type[DndClass], character_level: Optional[int] = None):
        if character_level is None:
            return len(list(filter(lambda dc: isinstance(dc, dnd_class), self)))
        return len(list(filter(lambda dc: isinstance(dc, dnd_class), self[:character_level])))

    def append(self, dnd_class: Type[DndClass]):
        super().append(dnd_class(self.character, self.class_level(dnd_class) + 1))
        self._update_hit_points()

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
        super().__setitem__(key, dnd_class(self.character, self.class_level(dnd_class, key + 1) + 1))
        for item in self[key+1:]:
            if isinstance(item, dnd_class):
                item.level += 1
        self._update_hit_points()

    def insert(self, index: int, dnd_class: Type[DndClass]):
        super().insert(index, dnd_class(self.character, self.class_level(dnd_class, index + 1) + 1))
        for item in self[index+1:]:
            if isinstance(item, dnd_class):
                item.level += 1
        self._update_hit_points()

    def all(self, character_level: Optional[int] = None):
        cur = {}
        if character_level is None:
            return self
        else:
            return self[:character_level]

    def current(self, character_level: Optional[int] = None):
        cur = {}
        for cls in self.all(character_level):
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
        self.classes = ClassProgression(self)
        self.feats = {}  # type: Dict[int, Feat]
        self.flaws = {}  # type: Dict[int, Flaw]
        self.abilities = AbilityProgression()
        self.race = race(self)

    def level_up(self, dnd_class: Type[DndClass]):
        self.classes.append(dnd_class)

    def hit_points(self, level: Optional[int] = None):
        return

    @property
    def level(self):
        return len(self.classes)

    def _aspects(self, level: Optional[int] = None):
        return self.classes.current(level) + [self.race]

    def hit_die(self, level: Optional[int] = None):
        classes = self.classes.all(level)
        hd = Roll()
        if len(classes) > 0:
            hd.append(classes[0].hit_die.sides)
            if len(classes) > 1:
                hd.extend([item.hit_die for item in classes[1:]])
        return hd

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
        lines.append("  Lvl BaB Fort Ref Will Class      HD")
        for lvl in range(1, self.level+1):
            lines.append(f"  {lvl:>2}: "
                         f"{self.base_attack_bonus(lvl):^3} "
                         f"{self.fortitude_save(lvl):^4} "
                         f"{self.reflex_save(lvl):^3} "
                         f"{self.will_save(lvl):^4} "
                         f"{self.classes[lvl-1]:<10} "
                         f"{self.hit_die(lvl)}"
                         )
        return "\n".join(lines)
