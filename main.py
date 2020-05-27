import curses
import json
import os
import string
from world import *


if not os.path.exists("campaign.json"):
    world = Location(name="The World")
    continent = Location(name="The Continent", location=world)
    kingdom = Location(name="The Kingdom", location=continent)
    city = Location(name="The City", location=kingdom)
    tavern = Location(name="The Tavern", location=city)

    arrival = Passage(location=city, body="""
The party arrives in {location:1} by way of a {tribe} caravan under the guidance of {caravan_leader}.
    """)
    arrival.tribe = "Go'Val"
    arrival.caravan_leader = "Maran"

    with open("campaign.json", "w") as fl:
        json.dump(to_json(arrival, tavern), fl)


class UI:
    def __init__(self, screen=None):
        self.screen = screen
        self.objects = WorldObject._extract_objects_from_json(json.load(open("campaign.json")))
        self._current_object = Location(name="The Universe")
        for root in list(sorted(filter(lambda o: o.location is None, self.objects.values()), key=lambda o: o.object_id)):
            self.current_object.add_child_locatable(root)
        self._locations = list(filter(lambda o: isinstance(o, Location), self.current_object._child_locatables))
        self.current_object_pad = None
        self.locations_pad = None
        self.story_pad = None
        if self.screen:
            self.init_screen()
            self.main()
        # else:
        #     [print(o) for o in self.objects.values()]
        #     print(self.current_object)
        #     [print(o) for o in self.current_object._child_locatables]

    def init_screen(self):
        self.screen.clear()
        self.screen.refresh()
        self.current_object_pad = curses.newpad(3, 50)
        self.locations_pad = curses.newpad(50, 50)
        self.story_pad = curses.newpad(50, 50)
        self._refresh_current_object_pad()
        self._refresh_locations_pad()

    @property
    def current_object(self):
        return self._current_object
    
    @current_object.setter
    def current_object(self, current_object):
        self._current_object = current_object
        self._refresh_current_object_pad()
        self.locations = list(filter(lambda o: isinstance(o, Location), self.current_object._child_locatables))

    def _refresh_current_object_pad(self):
        self.current_object_pad.clear()
        self.current_object_pad.addstr(1, 2, f"{self.current_object:1}")
        print("Refreshing current object pad")
        self.current_object_pad.border()
        self.current_object_pad.refresh(
            0,  0,  # Pad Top Left
            0,  0,  # Win Top Left
           10, 50,  # Win Bottom Right
        )

    @property
    def locations(self):
        return self._locations

    @locations.setter
    def locations(self, locations):
        self._locations = locations
        self._refresh_locations_pad()
    
    def _refresh_locations_pad(self):
        self.locations_pad.clear()
        for i, location in enumerate(self.locations):
            self.locations_pad.addstr(i+1, 2, f"{i:>2}: {location:0}")
        self.locations_pad.border()
        self.locations_pad.refresh(
             0,  0,  # Pad Top Left
             3,  0,  # Win Top Left
            10, 50,  # Win Bottom Right
        )
        self.screen.move(4, 3)

    def main(self):
        selected_index = 0
        while True:
            self.screen.move(4, 3 + selected_index)
            key = self.screen.getkey()
            if key in {"q", "Q"}:
                break
            elif key in {curses.KEY_UP, "w", "W"}:
                selected_index = max(0, selected_index-1)
            elif key in {curses.KEY_DOWN, "s", "S"}:
                selected_index = min(len(self.current_object._child_locatables), selected_index+1)
            elif key in {curses.KEY_LEFT, "a", "A"}:
                if self.current_object.location:
                    self.current_object = self.current_object.location
            elif key in {curses.KEY_RIGHT, "d", "D"}:
                if 0 <= selected_index < len(self.locations):
                    self.current_object = self.locations[selected_index]

curses.wrapper(UI)
# UI()
