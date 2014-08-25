from uuid import uuid4
from tkinter import Label

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
    Label.__init__(self,character,height=20,width=100)
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

