from tkinter import Tk,Frame,Label,Button
from weapons import MasterworkScimitar
from characterbase import Character,Title
from random import randint

class dndgui(Tk):
  def __init__(self):
    Tk.__init__(self)
    self.title('D&D GUI')
    self.pack_propagate(0)
    self.config(height=500,width=500)
    self.mButton = Button(self,height=2,width=16,text='Run',command=self.Run)
    self.mButton.place(x=0,y=0)
    self.mHit = Label(self,text='-----------',width=11)
    self.mHit.place(x=0,y=50)
    self.mDamage = Label(self,text='---',width=3)
    self.mDamage.place(x=80,y=50)
    self.mAC = Label(self,text='---',width=3)
    self.mAC.place(x=100,y=50)

    self.mChar = Character(self,name='Baship',titles=[Title('Eldricht Knight')])
    self.mChar.mActiveWeapon = MasterworkScimitar()
  def Run(self):
    print(self.mChar.mName)
    ac = randint(5,25)
    self.mAC.config(text=str(ac))
    hit = self.mChar.calcHit(3,ac)
    crit = hit[0]=='Crit'
    hitStr = ','.join([str(s) for s in hit])
    self.mHit.config(text=hitStr)
    if hit[0] != 'Miss':
      self.mDamage.config(text=str(self.mChar.mActiveWeapon.calcDamage(crit)))
    else:
      self.mDamage.config(text='0')

if __name__ == '__main__':
  root = dndgui()
  root.mainloop()
#  print(self.winfo_height(),self.winfo_width())
