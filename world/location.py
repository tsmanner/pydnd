import json
from os import linesep
import re
from string import Formatter
from typing import Iterable, List, Optional, Set, Union

from world.world_object import WorldObject


def recursive_format(s, o):
    if s and o:
        body = linesep.join([line.replace(linesep, ' ') for line in s.split(f"{linesep}{linesep}")])
        return body.format(**
            {
                key: getattr(o, key) for key in map(
                    lambda t: t[1].split(".")[0],
                    filter(lambda t: t[1], Formatter().parse(body))
                )
            }
        )
    return "<No Description>"


class Locatable(WorldObject):
    def __init__(self, *, object_id: int = None, location: "Location" = None, description: Optional[Union[str, "Passage"]] = None, **kwargs):
        super().__init__(object_id, **kwargs)
        self._parent_location = None  # type: Locatable
        self._child_locatables = []  # type: List[Locatable]
        self.location_history = []  # type: List[Locatable]
        self.location = location
        self.description = description
        if isinstance(self.description, Passage):
            self.description.location = self

    @property
    def location(self):
        return self._parent_location

    @location.setter
    def location(self, location: "Location"):
        if self.location is not None:
            self.location_history.append(self._parent_location)
        self._parent_location = location
        if isinstance(self._parent_location, Location):
            self._parent_location._child_locatables.append(self)

    @location.deleter
    def location(self):
        if self.location is not None:
            self.location_history.append(self._parent_location)
            self.location._child_locatables.remove(self)
            self._parent_location = None


class NamedLocatable(Locatable):
    def __init__(self, *, name: str = "<Name Not Set>", **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def __format__(self, format_spec=''):
        return self.name

    def __str__(self):
        return format(self)

    def __repr__(self):
        return f"<{type(self).__name__}({self.object_id}): {self.name}>"


class Location(NamedLocatable):
    def __format__(self, format_spec = ''):
        """ A Location's format_spec can only be an integer, representing
            how many levels of hierarchy to traverse """
        class Depth:
            def __init__(self, depth_spec):
                try:
                    self.depth = int(depth_spec)
                except:
                    self.depth = None

            def __str__(self):
                return str(self.depth) if self.depth is not None else ''

            def __repr__(self):
                return str(self)

            def __bool__(self):
                return self.depth is None or self.depth > 0

            def __sub__(self, other):
                return self if self.depth in {None, 0} else Depth(self.depth - 1)

        depth = Depth(format_spec)
        if depth:
            if isinstance(self.location, Location):
                return f"{self.name}, {self.location:{depth-1}}"
            elif self.location is not None:
                return f"{self.name}, {self.location}"
        return self.name

    def __str__(self):
        return format(self, "1")


class Passage(NamedLocatable):
    latest_passage = None

    def __init__(self, *, body: str = "", previous_passage: "Passage" = None, **kwargs):
        super().__init__(**kwargs)
        self._previous_passage = None
        self._next_passage = None
        self.previous_passage = previous_passage if previous_passage else Passage.latest_passage
        self.body = body.strip()
        Passage.latest_passage = self

    def __setattr__(self, name, value):
        if not hasattr(self, "references"):
            super().__setattr__("references", [])
        if isinstance(value, WorldObject) and value not in self.references:
            self.references.append(value)
        super().__setattr__(name, value)

    @property
    def previous_passage(self):
        return self._previous_passage

    @previous_passage.setter
    def previous_passage(self, previous_passage):
        # If this Passage already has a previous Passage, put the new one
        # in between that Passage and self.
        # 1. Set the new previous Passage's previous reference to our old one
        # 2. Set the new previous Passage's next reference to self
        # 3. Set self's previous reference to the new previous Passage
        if previous_passage:
            if self._previous_passage:
                previous_passage.previous_passage = self.previous_passage
            previous_passage._next_passage = self
        self._previous_passage = previous_passage

    def _format(self, s):
        return recursive_format(self.body, self)

    def __format__(self, *_, **__):
        return self._format(self.body)

    def __str__(self):
        return self._format(self.name)

