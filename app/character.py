from collections import defaultdict
from functools import reduce
from typing import DefaultDict, Dict, List, Optional, Type, Union
from app.base import *
from app.classes import *
from app.feat import *
from app.races import *


class BonusProgression:
    def __init__(self, character: "Character"):
        self._bonuses = {}
        self.character = character

    def __getitem__(self, level: Union[int, None]):
        if level is None:
            level = self.character.level()
        key = level - 1
        filtered = list(filter(lambda k: k <= key, self._bonuses.keys()))
        if len(filtered) > 0:
            return self._bonuses[max(filtered)]
        self._bonuses[level] = DndBase()
        return self._bonuses[level]

    def __setitem__(self, level: int, value: DndBase):
        key = level - 1
        self._bonuses[key] = value


class ClassProgression(list):
    def __init__(self, character: "Character"):
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

    def append(self, dnd_class: Type[DndClass], **kwargs):
        super().append(dnd_class(self.character, self.class_level(dnd_class) + 1, **kwargs))
        self._update_hit_points()

    def __setitem__(self, key: int, dnd_class: Type[DndClass]):
        """ Replace a character level with a different class.
        1) Decrement the level of all subsequent instances of the old class
        2) Insert the new class instance
        3) Increment the level of all subsequent instances of the new class
        """
        old_type = type(super()[key])
        for item in self[key + 1:]:
            if isinstance(item, old_type):
                item.level -= 1
        super().__setitem__(key, dnd_class(self.class_level(dnd_class, key + 1) + 1))
        for item in self[key + 1:]:
            if isinstance(item, dnd_class):
                item.level += 1
        self._update_hit_points()

    def insert(self, index: int, dnd_class: Type[DndClass]):
        super().insert(index, dnd_class(self.class_level(dnd_class, index + 1) + 1))
        for item in self[index + 1:]:
            if isinstance(item, dnd_class):
                item.level += 1
        self._update_hit_points()

    def all(self, character_level: Optional[int] = None):
        if character_level is None:
            return self
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


class Character(DndBase):
    save_links = {
        "armor_class": "dexterity",
        "fear": "will",
        "fortitude": "constitution",
        "reflex": "dexterity",
        "will": "wisdom",
    }

    def __init__(self, race: Type[Race]):
        super().__init__()
        self.armor_class.append(10, "base")
        self.classes = ClassProgression(self)
        self.level_bonuses = BonusProgression(self)
        self.feats = defaultdict(list)  # type: DefaultDict[int, Feat]
        self.flaws = []  # type: List[Flaw]
        self.race = race()
        self.equipment = []  # type: List[DndBase]

    def level_up(self, dnd_class: Type[DndClass],
                 bonuses: Optional[Dict[str, int]] = None):
        self.classes.append(dnd_class)
        if bonuses is not None:
            self.level_bonuses[self.level()] = DndBase()
            [self.level_bonuses[self.level()].__getattribute__(k).append(bonuses[k], "level") for k in bonuses]

    def level(self, dnd_class: Optional[Type[DndClass]] = None):
        if dnd_class is not None:
            return len(list(filter(lambda c: isinstance(c, dnd_class), self.classes)))
        return len(self.classes)

    def _aspects(self, level: Optional[int] = None):
        if level is not None:
            feats = reduce(lambda a, b: a + b, [self.feats[k] for k in filter(lambda l: l <= level, self.feats)], [])
        else:
            feats = []
        return self.classes.current(level) + \
               [self.level_bonuses[level], self.race] + \
               self.equipment + \
               feats + \
               self.flaws

    def hit_die(self, level: Optional[int] = None):
        classes = self.classes.all(level)
        hd = Roll()
        if len(classes) > 0:
            hd.append(classes[0].hit_die.sides)
            if len(classes) > 1:
                hd.extend([item.hit_die for item in classes[1:]])
        return hd

    def _bonus(self, field: str, level: Optional[int] = None):
        items = [item.__getattribute__(field) for item in self._aspects(level)]
        items.append(self.__getattribute__(field))
        return items

    def bonus(self, field: str, level: Optional[int] = None):
        items = self._bonus(field, level)
        return reduce(lambda a, b: a + b, items[1:], items[0])

    def _save(self, field: str, level: Optional[int] = None):
        items = [item.__getattribute__(field) for item in self._aspects(level)]
        items.append(self.__getattribute__(field))
        if field in Character.save_links:
            linked = Character.save_links[field]
            if linked in DndBase.Abilities:
                items.append(self.bonus(linked, level))
            else:
                items.extend(self._save(linked, level))
        return items

    def save(self, field: str, level: Optional[int] = None):
        return sum(self._save(field, level))

    def base_attack_bonus(self, level: Optional[int] = None):
        return sum([item.attack["base"] for item in self._aspects(level)])

    def fortitude_save(self, level: Optional[int] = None):
        return sum([item.save["fortitude"] for item in self._aspects(level)])

    def reflex_save(self, level: Optional[int] = None):
        return sum([item.save["reflex"] for item in self._aspects(level)])

    def will_save(self, level: Optional[int] = None):
        return sum([item.save["will"] for item in self._aspects(level)])

    def __str__(self, verbose: bool = False):
        lines = [
            f"Level {self.level()} {self.race} {'/'.join([str(c) for c in self.classes.current()])}",
            f"AC: {self.save('armor_class'):^2}"
        ]
        if verbose:
            lines.append(f"Equipped: {', '.join([str(item) for item in self.equipment])}")
        if self.level() == 0:
            return lines[0]
        if verbose:
            class_width = max([len(str(item)) for item in self.classes])
        else:
            class_width = len(str(self.classes[-1]))
        hd_width = max([len(str(self.hit_die(lvl + 1))) for lvl in range(self.level())])
        stat_width = 6
        lines.append(f"  Lvl"
                     f" {'Str':^{stat_width}}"
                     f" {'Dex':^{stat_width}}"
                     f" {'Con':^{stat_width}}"
                     f" {'Int':^{stat_width}}"
                     f" {'Wis':^{stat_width}}"
                     f" {'Cha':^{stat_width}}"
                     f" BaB"
                     f" Fort"
                     f" Ref"
                     f" Will "
                     f" {'Class':<{class_width}}"
                     f" {'HD':<{hd_width}}"
                     f" Feats")
        if verbose:
            for lvl in range(1, self.level() + 1):
                lines.append(f"  {lvl:>2}:"
                             f" {self.bonus('strength', lvl):^{stat_width}}"
                             f" {self.bonus('dexterity', lvl):^{stat_width}}"
                             f" {self.bonus('constitution', lvl):^{stat_width}}"
                             f" {self.bonus('intelligence', lvl):^{stat_width}}"
                             f" {self.bonus('wisdom', lvl):^{stat_width}}"
                             f" {self.bonus('charisma', lvl):^{stat_width}}"
                             f" {self.base_attack_bonus(lvl):^3}"
                             f" {self.save('fortitude', lvl):^4}"
                             f" {self.save('reflex', lvl):^4}"
                             f" {self.save('will', lvl):^4}"
                             f" {self.classes[lvl-1]:<{class_width}}"
                             f" {self.hit_die(lvl):<{hd_width}}"
                             f" {self.feats[lvl]}"
                             )
        else:
            lines.append(f"  {self.level():>2}:"
                         f" {self.bonus('strength'):^{stat_width}}"
                         f" {self.bonus('dexterity'):^{stat_width}}"
                         f" {self.bonus('constitution'):^{stat_width}}"
                         f" {self.bonus('intelligence'):^{stat_width}}"
                         f" {self.bonus('wisdom'):^{stat_width}}"
                         f" {self.bonus('charisma'):^{stat_width}}"
                         f" {self.base_attack_bonu:^3}"
                         f" {self.save('fortitude'):^4}"
                         f" {self.save('reflex'):^4}"
                         f" {self.save('will'):^4}"
                         f" {self.classes[-1]:<{class_width}}"
                         f" {self.hit_die()}"
                         f" {self.feats[self.level()]}"
                         )

        return "\n".join(lines)
