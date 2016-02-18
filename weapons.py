import dndtypes
import random

NO_DAMAGE = -1
SLASH = 0
PIERCE = 1
BLUDGEON = 2


class Weapon(dndtypes.Equipment):
    def __init__(self,
                 attack_bonus: int,
                 base_damage: int,
                 damage_rolls: list,
                 critical: int,
                 damage_type: int,
                 attack_range: int,
                 notes: str,
                 id_num: int):
        dndtypes.Equipment.__init__(self, id_num=id_num)
        self.attack_bonus = attack_bonus
        self.base_damage = base_damage
        self.damage_rolls = damage_rolls
        self.critical = critical
        self.damage_type = damage_type
        self.attack_range = attack_range
        self.notes = notes

    @property
    def damage(self):
        return self.base_damage + sum([random.randint(1, x) for x in self.damage_rolls])


class MeleeWeapon(Weapon):
    def __init__(self,
                 attack_bonus,
                 base_damage,
                 damage_rolls,
                 critical,
                 damage_type,
                 notes,
                 id_num):
        Weapon.__init__(self,
                        attack_bonus=attack_bonus,
                        base_damage=base_damage,
                        damage_rolls=damage_rolls,
                        critical=critical,
                        damage_type=damage_type,
                        attack_range=5,
                        notes=notes,
                        id_num=id_num)


class RangedWeapon(Weapon):
    def __init__(self):
        Weapon.__init__(self)


class Ammunition(Weapon):
    def __init__(self):
        Weapon.__init__()


class Slasher(MeleeWeapon):
    def __init__(self,
                 attack_bonus,
                 base_damage,
                 damage_rolls,
                 critical,
                 notes,
                 id_num):
        MeleeWeapon.__init__(self,
                             attack_bonus=attack_bonus,
                             base_damage=base_damage,
                             damage_rolls=damage_rolls,
                             critical=critical,
                             damage_type=SLASH,
                             notes=notes,
                             id_num=id_num)


class Piercer(MeleeWeapon):
    def __init__(self,
                 attack_bonus,
                 base_damage,
                 damage_rolls,
                 critical,
                 notes,
                 id_num):
        MeleeWeapon.__init__(self,
                             attack_bonus,
                             base_damage,
                             damage_rolls,
                             critical,
                             damage_type=PIERCE,
                             notes=notes,
                             id_num=id_num)


class Bludgeon(MeleeWeapon):
    def __init__(self,
                 attack_bonus,
                 base_damage,
                 damage_rolls,
                 critical,
                 notes,
                 id_num):
        MeleeWeapon.__init__(self,
                             attack_bonus,
                             base_damage,
                             damage_rolls,
                             critical,
                             damage_type=BLUDGEON,
                             notes=notes,
                             id_num=id_num)


class LightWeapon:
    def __init__(self):
        self.hands = 1
        self.two_hand_modifier = 1.0


class OneHandWeapon:
    def __init__(self):
        self.hands = 1
        self.two_hand_modifier = 1.5


class TwoHandWeapon:
    def __init__(self):
        self.hands = 2
        self.two_hand_modifier = 1.5

"""
Specific Weapons:
    Unarmed
    MasterwokScimitar
"""


class Unarmed(Bludgeon):
    def __init__(self, notes='', id_num=-1):
        Bludgeon.__init__(self,
                          attack_bonus=0,
                          base_damage=0,
                          damage_rolls=[4],
                          critical=20,
                          notes=notes,
                          id_num=id_num)


class MasterworkScimitar(OneHandWeapon, Slasher):
    def __init__(self, notes='', id_num=-1):
        OneHandWeapon.__init__(self)
        Slasher.__init__(self,
                         attack_bonus=2,
                         base_damage=1,
                         damage_rolls=[4],
                         critical=18,
                         notes=notes,
                         id_num=id_num)
