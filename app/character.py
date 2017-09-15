from collections import defaultdict
from functools import reduce
from typing import DefaultDict, Dict, List, Optional, Type, Union
from app.base import *
from app.classes import *
from app.feat import *
from app.races import *


class CharacterLevel(DndBase):
    def __init__(self, character: "Character", dnd_class: Type[DndClass]):
        super().__init__()
        self.character = character
        self.armor_class.append(10, "base")
        self.feats = []  # type: List[Feat]
        self.flaws = []  # type: List[Flaw]
        self.dnd_class = dnd_class

    def _aspects(self):
        feats = reduce(lambda a, b: a + b.feats, self.character.levels[0:self.level], [])
        flaws = reduce(lambda a, b: a + b.flaws, self.character.levels[0:self.level], [])
        return [self, self.dnd_class(self, self.level)] + feats + flaws

    @property
    def level(self):
        return self.character.levels.index(self) + 1


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
        # self.armor_class.append(10, "base")
        self.levels = []  # type: List[CharacterLevel]
        # self.classes = ClassProgression(self)
        # self.level_bonuses = BonusProgression(self)
        # self.feats = defaultdict(list)  # type: DefaultDict[int, Feat]
        # self.flaws = []  # type: List[Flaw]
        self.race = race()
        self.equipment = []  # type: List[DndBase]

    def level_up(self, dnd_class: Type[DndClass],
                 bonuses: Optional[Dict[str, int]] = None):
        self.levels.append(CharacterLevel(self, dnd_class))
        # self.classes.append(dnd_class)
        # if bonuses is not None:
        #     self.level_bonuses[self.level()] = DndBase()
        #     [self.level_bonuses[self.level()].__getattribute__(k).append(bonuses[k], "level") for k in bonuses]

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

    def summary(self):
        return f"Level {self.level()} {self.race} {'/'.join([str(c) for c in self.classes.current()])}"

    def __str__(self, verbose: bool = False):
        lines = [
            self.summary(),
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
