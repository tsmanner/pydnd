import character
import classes
import collections
import dndtypes
import os
import races
import sqlite3 as sql
import tkinter as tk
import weapons


class DndGui(tk.Frame):
    def __init__(self, master):
        # Initial setup of master window(self)
        tk.Frame.__init__(self, master)
        master.title('D&D GUI')
        self.db = 'dnd.db'
        self.init_db()
        # Setup Character data
        self.char = character.Character(name='Baship',
                                        titles='Eldricht Knight|Keeper of the Jars',
                                        height=37,
                                        weight=45,
                                        looks="Ruggedly Handsome",
                                        race="Strongheart Halfling",
                                        gender=character.MALE,
                                        character_class="Druid",
                                        class_level=1,
                                        alignment="Neutral Good",
                                        hit_point_max=90,
                                        initiative=2,
                                        speed=25,
                                        armor_class=4,
                                        attack_bonus=3)
        self.char.inventory.append(weapons.MasterworkScimitar())
        self.char.name.select_title(1)
        self.char.equip(weapons.MasterworkScimitar())
        self.save()

        self.priority_button = tk.Button(self, text="Calculate Priority", command=self.calc_priority)
        self.priority_button.pack(side=tk.TOP)
        self.turn_order_list = tk.Listbox(self, font="courier 9", height=10, width=50)
        self.turn_order_list.pack(side=tk.TOP)
        self.load()

    def calc_priority(self, event=None):
        priority_map = collections.defaultdict(list)
        for char in character.characters.values():
            priority_map[char.roll_initiative()].append(char)
        self.turn_order_list.delete(0, tk.END)
        [[self.turn_order_list.insert(tk.END, char) for char in priority_map[priority]]
         for priority in priority_map]

    def attack(self, event=None):
        print(self.char.attack(self.enemy))

    def load(self):
        with sql.connect(self.db) as conn:
            [print(character.Character(*list(row))) for row in conn.execute("SELECT * FROM Characters").fetchall()]

    def save(self):
        os.remove(self.db)
        self.init_db()
        with sql.connect(self.db) as conn:
            for char in character.characters.values():
                titles = '|'.join([title.title for title in char.name.titles])
                conn.execute("INSERT INTO Characters VALUES (" + ', '.join(['?'] * 16) + ")",
                             (char.name.name, titles, char.height, char.weight, char.looks,
                              char.race.name, char.gender, char.character_class.name,
                              char.character_class.level,
                              str(char.alignment), char.hit_point_max, char.initiative, char.speed,
                              char.armor_class,
                              char.attack_bonus,
                              str(char.id)))
            conn.commit()

    def init_db(self):
        if not os.path.exists(self.db):
            open(self.db, 'x')
        with sql.connect(self.db) as conn:
            columns = ['name TEXT',
                       'titles TEXT',
                       'height REAL',
                       'weight REAL',
                       'looks TEXT',
                       'race TEXT',
                       'gender TEXT',
                       'character_class TEXT',
                       'class_level INTEGER',
                       'alignment TEXT',
                       'hit_point_max INTEGER',
                       'initiative INTEGER',
                       'speed INTEGER',
                       'armor_class INTEGER',
                       'attack_bonus INTEGER',
                       'id_num TEXT']
            conn.execute("CREATE TABLE IF NOT EXISTS Characters(" + ', '.join(columns) + ")")
            conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    gui = DndGui(root)
    gui.config(height=500, width=500)
    gui.pack()
    root.mainloop()
