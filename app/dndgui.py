import tkinter as tk
from typing import Type
from app import *


class TkCharacter(Character, tk.Frame):
    def __init__(self, race: Type[Race], *args, **kwargs):
        print(args)
        print(kwargs)
        super().__init__(*args, race=race, **kwargs)


class DndGui(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.character = TkCharacter(Halfling, self)
        self.character.pack()


if __name__ == '__main__':
    root = tk.Tk()
    gui = DndGui(root)
    gui.pack()
    # root.mainloop()
    # char = TkCharacter(Halfling)
    # char.level_up(Wizard)
    # print(char)
