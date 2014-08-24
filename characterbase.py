from weapons import *
from armor import *
from random import randint
from tkinter import Frame,Label

class Text(Label):
  def __init__(self,master,text):
    Label.__init__(self, master)
    self.mText = text
  def __str__(self):
    return self.mText

class Title:
  def __init__(self,title=None,after=False):
    self.mTitle = title
    self.mAfter = after
  def addTitle(self,name):
    if self.mAfter:
      return name + ', ' + self.mTitle
    return self.mTitle + ' ' + name

class FullName(Label):
  def __init__(self,character,name,titles):
    Label.__init__(self,character)
    self.mName = name
    self.mInactiveTitles = titles
    if len(titles):
      self.mActiveTitle = titles[0]
    else:
      self.mActiveTitle = None
    self.config(text=str(self))
  def __str__(self):
    if self.mActiveTitle:
      return self.mActiveTitle.addTitle(self.mName)
    return self.mName

class Alignment:
  def __init__(self):
    # Lawful, Neutral, Chaotic
    self.mEthics = None
    # Good, Neutral, Evil
    self.mMorality = None

class Class:
  def __init__(self):
    self.mName = None
    self.mLevel = None

class Character(Frame):
  def __init__(self,master,name=None,titles=[],height=None,weight=None,looks=None, \
             race=None,gender=None,size=None,cls=Class(),alignment=Alignment()):
    Frame.__init__(self, master)
    # Character Info
    self.mName = FullName(self,name,titles)
    self.mHeight = height
    self.mWeight = weight
    self.mLooks = looks
    self.mRace = race
    self.mGender = gender
    self.mSize = size
    self.mClass = cls
    self.mAlignment = alignment
    # Ability Scores
    # Combat Options
    self.mAttackBonus = 0
    self.mActiveWeapon = Unarmed()
    self.mInactiveWeapons = []
    # Saving Throws
    # Armor Class
    # Spells
  def getName(self):
    if self.mActiveTitle:
      return self.mActiveTitle.addTitle(self.mName)
    return self.mName
  def calcHit(self,attackbonus,armorclass):
    bonus = self.mAttackBonus
    if self.mActiveWeapon:
      bonus += self.mActiveWeapon.mAttackBonus
    hitroll = randint(1,20)
    hit = hitroll + bonus
    # Did we register a hit?
    if hit >= armorclass:
      if hitroll >= self.mActiveWeapon.mCritical:
        critroll = randint(1,20)
        crit = critroll + bonus
        if crit > armorclass:
          return ('Crit',hitroll,crit)
      return ('Hit',hit)
    return ('Miss',hit)

