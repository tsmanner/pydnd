from dndlib import Character,Title
from weapons import MasterworkScimitar
'''
class Character:
  def __init(self):
    self.mName = None
    self.mTitles = []
    self.mActiveTitle = None
    self.mHeight = None
    self.mWeight = None
    self.mLooks = None
    self.mRace = None
    self.mGender = None
    self.mSize = None
    self.mClass = Class()
    self.mAlignment = Alignment()
'''

#myTitles = [Title('Eldricht Knight'),Title('Keeper of the Jars',True)]
#c = Character(name='Baship',titles=myTitles)
#c.mActiveTitle = c.mTitles[1]
#print(c.getName())
s = MasterworkScimitar()
print(s.calcHit())
print(s.calcDamage())
