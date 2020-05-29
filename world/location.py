import json
from os import linesep
import re
from string import Formatter
from typing import Iterable, List, Optional, Set, Union

from world.world_object import WorldObject


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

    def __repr__(self):
        return format(self)


class Passage(NamedLocatable):
    def __init__(self, *, body: str = "", prev: "Passage" = None, **kwargs):
        super().__init__(**kwargs)
        self.body = body.strip()
        self._prev = None
        self.prev = prev
        self.next = None
        self.references = {}

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, prev):
        self._prev = prev
        if self._prev and self._prev.next:
            self.next = self._prev.next
            self.next._prev = self
        if self._prev:
            self._prev.next = self

    def _format(self, s):
        body = linesep.join([line.replace(linesep, ' ') for line in s.split(f"{linesep}{linesep}")])
        kvs = {key[1]: getattr(self, key[1]) for key in filter(lambda t: t[1] is not None, Formatter().parse(body))}
        return body.format(
            **kvs
        )

    def __format__(self, *_, **__):
        return self._format(self.body)

    def __str__(self):
        return self._format(self.name)

