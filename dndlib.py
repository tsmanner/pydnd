'''
Data:
  Character
    Player Name
    Name
    Title
    Race
    Size
    Gender
    Height
    Weight
    Looks
    Class
    Level
    Alignment
    Religion/Patron Deity
  Ability Scores
    Strength
    Dexterity
    Constitution
    Intellect
    Wisdom
    Charisma
    Speed
    Initiative Modifier
    Grapple Modifier
  Combat Options
    Base Attack Bonus
    Weapons
  Saving Throws
    Fortitude
    Reflex
    Will
  Armor Class
    Armor Class
    Touch Armor Class
    Flat-Footed Armor Class
    Armor Worn
    Shield Carried
  Magic
  Spells
  Turn/Rebuke Undead
  Psionics
  Rage
  Animal Companion/Familiar, or Psicystal
  Skills
  Racial Traits/Class Features
  Feats
  Languages
  Skill Synergies
  Gear
'''

from uuid import uuid4

class Spell:
  def __init__(self):
    self.mName = None
    self.mCastTime = None
    self.mRange = None
    self.mEffect = None
    self.mDuration = None
    self.mSavingThrow = None
    self.mSpellResistance = None
    self.mLevel = None

class Item:
  def __init__(self):
    self.mId = uuid4()

