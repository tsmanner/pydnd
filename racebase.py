from tkinter import Label

SMALL = 0
MEDUIUM = 1
LARGE = 2

class Race(Label):
  def __init__(self, master,size):
    Label.__init__(self, master)
    self.mSize = size
