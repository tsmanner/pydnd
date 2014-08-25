from weaponbase import Slasher,Bludgeon,Piercer

class MasterworkScimitar(Slasher):
  def __init__(self,notes=None):
    Slasher.__init__(self,attackBonus=2,baseDamage=1,damageRolls=[4],critical=18,notes=notes)

class Unarmed(Bludgeon):
  def __init__(self,notes=None):
    Bludgeon.__init__(self,attackBonus=0,baseDamage=0,damageRolls=[4],critical=20,notes=notes)

