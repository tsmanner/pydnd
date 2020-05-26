from os import linesep
from string import Formatter
from typing import List, Set


def _generate_id():
    next_id = 0
    while True:
        yield next_id
        next_id += 1


def jsonify(objects, *world_objects):
    objects = {}
    for world_object in world_objects:
        objects[hash(world_object)] = world_object.__json__()
        for attr in world_object._attrs:
            if isinstance(getattr(world_object, attr), WorldObject):
                jsonify(getattr(world_object, attr))
    return objects


class WorldObject:
    def __init__(self, object_id=None):
        super().__init__()
        super().__setattr__("_attrs", set())
        self.object_id = object_id if object_id is not None else next(WorldObject.ObjectID)

    def __setattr__(self, name, value):
        self._attrs.add(name)
        super().__setattr__(name, value)

    def __json__(self):
        print(
            {
                attr: getattr(self, attr)
                for attr in self._attrs
            }
        )

    def __hash__(self):
        return hash(hash(type(self).__name__) + hash(self.object_id))

    ObjectID = _generate_id()


class Locatable(WorldObject):
    def __init__(self, *, object_id=None, location: "Location" = None):
        super().__init__(object_id)
        self._parent_location = None  # type: Locatable
        self._child_locatables = set()  # type: Set[Locatable]
        self.location_history = []  # type: List[Locatable]
        self.location = location

    @property
    def location(self):
        return self._parent_location

    @location.setter
    def location(self, location: "Location"):
        self.location_history.append(self._parent_location)
        self._parent_location = location
        if self.location is not None:
            self._parent_location._child_locatables.add(self)

    @location.deleter
    def location(self):
        if self.location is not None:
            self.location_history.append(self._parent_location)
            self._parent_location._child_locatables.remove(self)
            self._parent_location = None


class Location(Locatable):
    def __init__(self, name, parent_location: "Location" = None):
        super().__init__(location=parent_location)
        self.name = name

    def __iter__(self):
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

            def __bool__(self):
                return self.depth is None or self.depth > 0

            def __sub__(self, other):
                return self if self.depth in {None, 0} else Depth(self.depth - 1)

        depth = Depth(format_spec)
        if depth and self.location:
            return f"{self.name}, {self.location:{depth-1}}"
        return self.name

    def __str__(self):
        return format(self, 1)

    def __repr__(self):
        return format(self)


class Passage(Locatable):
    def __init__(self, location: Location, body: str):
        super().__init__(location=location)
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

world = Location("The World")
continent = Location("The Continent", world)
kingdom = Location("The Kingdom", continent)
city = Location("The City", kingdom)
tavern = Location("The Tavern", city)

arrival = Passage(city, """
The party arrives in {location:1} by way of a {tribe} caravan under the guidance of {caravan_leader}.
""")
arrival.tribe = "Go'Val"
arrival.caravan_leader = "Maran"

print(arrival)
print(arrival.__json__())
print()
