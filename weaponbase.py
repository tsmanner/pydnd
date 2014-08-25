from types import Item
from random import randint

SLASH = 0
PIERCE = 1
BLUDGEON = 2

class Weapon(Item):
  def __init__(self,attackBonus,baseDamage,damageRolls,critical,type,range,notes=None,ammunition=None):
    Item.__init__(self)
    self.mAttackBonus = attackBonus
    self.mBaseDamage = baseDamage
    self.mDamageRolls = damageRolls
    self.mCritical = critical
    self.mType = type
    self.mRange = range
    self.mNotes = notes
    self.mAmmunition = ammunition
  def calcDamage(self,critical=False):
    damage = self.mBaseDamage + sum([randint(1,x) for x in self.mDamageRolls])
    if critical:
      damage *= 2
    return damage

class MeleeWeapon(Weapon):
  def __init__(self,attackBonus,baseDamage,damageRolls,critical,type,notes=None):
    Weapon.__init__(self,attackBonus,baseDamage,damageRolls,critical,type,range=5,notes=notes)

class RangedWeapon(Weapon):
  def __init__(self):
    Weapon.__init__(self)

class Slasher(MeleeWeapon):
  def __init__(self,attackBonus,baseDamage,damageRolls,critical,notes=None):
    MeleeWeapon.__init__(self,attackBonus,baseDamage,damageRolls,critical,type=SLASH,notes=notes)

class Piercer(MeleeWeapon):
  def __init__(self,attackBonus,baseDamage,damageRolls,critical,notes=None):
    MeleeWeapon.__init__(self,attackBonus,baseDamage,damageRolls,critical,type=PIERCE,notes=notes)

class Bludgeon(MeleeWeapon):
  def __init__(self,attackBonus,baseDamage,damageRolls,critical,notes=None):
    MeleeWeapon.__init__(self,attackBonus,baseDamage,damageRolls,critical,type=BLUDGEON,notes=notes)

