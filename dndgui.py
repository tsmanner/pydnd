from tkinter import Tk,Frame,Label,Canvas
from weapons import MasterworkScimitar
from character import Character
from dndtypes import Title,Text
from races import StrongheartHalfling
from random import randint

class dndgui(Frame):
  def __init__(self,master):
    # Initial setup of master window(self)
    Frame.__init__(self,master)
    master.title('D&D GUI')
#    self.pack_propagate(0)
#    self.config(height=500,width=500)
    # Setup Character data
    self.mChar = Character(self,\
                 name='Baship',\
                 titles=[Title('Eldricht Knight'),Title('Keeper of the Jars',True)],\
                 height=37, weight=45,\
                 looks=Text(self,'Ruggedly Handsome'),\
                 race=StrongheartHalfling(self))
    self.mChar.mActiveWeapon = MasterworkScimitar()
    # Setup and place GUI elements
    self.placeElements()
  def placeElements(self):
    # Seed the x/y
    x = 0
    y = 0
    '''
    # h is the height and w is the width of the next thing being placed
    h = 50
    w = 100
    self.mButton = Canvas(self,height=h-4,width=w-4,bg='tan')
    self.mButton.bind("<Button-1>",self.Run)
    self.mButton.place(x=x,y=y)
    # Update x/y
    x += w
    y += h
    '''
    self.mChar.place(x=x,y=y)
    '''
    self.mHit = Label(self,text='-----------',width=11)
    self.mHit.place(x=0,y=100)
    self.mDamage = Label(self,text='---',width=3)
    self.mDamage.place(x=80,y=100)
    self.mAC = Label(self,text='---',width=3)
    self.mAC.place(x=100,y=100)
    '''

  def Run(self,event=None):
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
  root = Tk()
  gui = dndgui(root)
  gui.config(height=500,width=500)
  gui.pack()
  root.mainloop()
