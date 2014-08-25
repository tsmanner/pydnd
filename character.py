from random import randint
from tkinter import Frame,Label
from dndtypes import Class,Alignment,FullName
from weapons import Unarmed

class Character(Frame):
  def __init__(self,master,name=None,titles=[],height=None,weight=None,looks=None, \
             race=None,gender=None,size=None,cls=Class(),alignment=Alignment()):
    # Tkinter setup
    Frame.__init__(self, master, height=20, width=50)
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
  def placeElements(self):
    self.mName.place(x=0,y=0)
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

