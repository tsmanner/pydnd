import json
from os import linesep
import re
from string import Formatter
from typing import Iterable, List, Set, Union

from world.world_object import WorldObject


class Locatable(WorldObject):
    def __init__(self, *, object_id: int = None, location: "Location" = None):
        super().__init__(object_id)
        self._parent_location = None  # type: Locatable
        self._child_locatables = []  # type: List[Locatable]
        self.location_history = []  # type: List[Locatable]
        self.location = location

    @property
    def location(self):
        return self._parent_location

    @location.setter
    def location(self, location: "Location"):
        if self.location is not None:
            self.location_history.append(self._parent_location)
        self._parent_location = location
        if isinstance(self.location, Locatable):
            self._parent_location._child_locatables.append(self)

    @location.deleter
    def location(self):
        if self.location is not None:
            self.location_history.append(self._parent_location)
            self.location._child_locatables.remove(self)
            self._parent_location = None


class Location(Locatable):
    def __init__(self, *, name: str = '', **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def add_child_locatable(self, child):
        print(self, child)
        self._child_locatables.append(child)
        child.location = self

    def iter_child_locations(self):
        for location in self._child_locatables:
            yield location
            for child_location in location:
                yield child_location

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
        if depth and self.location:
            return f"{self.name}, {self.location:{depth-1}}"
        return self.name

    def __str__(self):
        return format(self, "1")

    def __repr__(self):
        return format(self)


class Passage(Locatable):
    def __init__(self, *, body: str = "", **kwargs):
        super().__init__(**kwargs)
        self.body = body.strip()
        self.references = {}

    def __format__(self, format_spec=None):
        body = ''.join([line.replace(linesep, '') for line in self.body.split(f"{linesep}{linesep}")])
        kvs = {key[1]: getattr(self, key[1]) for key in filter(lambda t: t[1] is not None, Formatter().parse(body))}
        return body.format(
            **kvs
        )

    def __str__(self):
        return format(self)

