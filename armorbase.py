from dndlib import Item

class Armor(Item):
  def __init__(self):
    Item.__init__(self)
    self.mMaxDex
    self.mArmorCheckPenalty
    self.mWeight

class Shield(Armor):
  def __init__(self):
    Armor.__init__(self)

