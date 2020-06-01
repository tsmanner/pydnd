from functools import reduce
from typing import List, Union
import world


def _generate_id():
    next_id = 0
    while True:
        yield next_id
        next_id += 1


class WorldObject:
    def __init__(self, object_id: int = None):
        super().__init__()
        self.object_id = object_id if object_id is not None else next(WorldObject.ObjectID)

    def __setattr__(self, name, value):
        # Don't capture properties (class level)
        if not hasattr(self, "_attrs"):
            super().__setattr__("_attrs",  set())
        if name not in dir(type(self)):
            self._attrs.add(name)
        super().__setattr__(name, value)

    @property
    def attrs(self):
        for attr_name in self._attrs:
            yield attr_name, getattr(self, attr_name)

    ObjectID = _generate_id()
