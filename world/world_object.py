import re
from typing import List, Union
import world


def _generate_id():
    next_id = 0
    while True:
        yield next_id
        next_id += 1


def to_json(*world_objects, objects=None):
    objects = {} if objects is None else objects
    for world_object in world_objects:
        world_object.__add_json_to__(objects)
    return objects


class WorldObject:
    class Reference:
        def __init__(self, object_or_string: Union["WorldObject", str]):
            if isinstance(object_or_string, str):
                match = re.match(r"WorldObject<(?P<object_type>\w+):(?P<object_id>-?\d+)>", object_or_string)
                if match is None:
                    raise ValueError(f"Could not parse reference string '{object_or_string}' into WorldObject.Reference")
                super().__setattr__("object", None)
                super().__setattr__("object_type", getattr(world, match["object_type"]))
                super().__setattr__("object_id", int(match["object_id"]))
            elif isinstance(object_or_string, WorldObject):
                super().__setattr__("object", object_or_string)
                super().__setattr__("object_type", type(object_or_string))
                super().__setattr__("object_id", object_or_string.object_id)
            else:
                raise ValueError(f"Could not parse {type(object_or_string).__name__} object '{object_or_string}' into WorldObject.Reference")

        def resolve(self, objects):
            super().__setattr__("object", objects[self.object_id])

        def __getattr__(self, name):
            return getattr(self.object, name)

        def __setattr__(self, name, value):
            return setattr(self.object, name, value)

        def __delattr__(self, name):
            return delattr(self.object, name)

        def __format__(self, format_spec = ''):
            if self.object is None or format_spec == "ref":
                return repr(self)
            return format(self.object, format_spec)

        def __repr__(self):
            return f"WorldObject<{self.object_type.__name__}:{self.object_id}>"

    def __init__(self, object_id: int = None):
        super().__init__()
        super().__setattr__("_attrs", set())
        self.object_id = object_id if object_id is not None else next(WorldObject.ObjectID)

    def __setattr__(self, name, value):
        self._attrs.add(name)
        if isinstance(value, WorldObject):
            value = WorldObject.Reference(value)
        super().__setattr__(name, value)

    @property
    def attrs(self):
        for attr_name in self._attrs:
            yield attr_name, getattr(self, attr_name)

    @staticmethod
    def _extract_objects_from_json(objects):
        python_objects = {}
        references = []
        for object_id_string in objects:
            object_id = int(object_id_string)
            new_object = getattr(world, objects[object_id_string]["object_type"])(object_id=object_id)
            # We do this in two passes:
            #     (1) Create all the toplevel objects, leaving the json_reference strings in place
            #     (2) Once all objects exist, resolve all json_reference strings to be actual object references
            for key, value in objects[object_id_string].items():
                if isinstance(value, List):
                    values = []
                    for item in value:
                        try:
                            values.append(WorldObject.Reference(item))
                            references.append(values[-1])
                        except ValueError:
                            values.append(item)
                    object.__setattr__(new_object, key, values)
                else:
                    try:
                        value = WorldObject.Reference(value)
                        references.append(value)
                    except ValueError:
                        pass
                    object.__setattr__(new_object, key, value)
            python_objects[object_id] = new_object
        for reference in references:
            reference.resolve(python_objects)
        return python_objects

    def __add_reference_json_to__(self, objects=None):
        if objects is not None and self.object_id not in objects:
            self.__add_json_to__(objects)
        return repr(type(self).Reference(self))

    def __add_json_to__(self, objects=None):
        objects = {} if objects is None else objects
        if self.object_id not in objects:
            objects[self.object_id] = { "object_type": type(self).__name__ }
            for name, value in self.attrs:
                if isinstance(value, (WorldObject, WorldObject.Reference)):
                    objects[self.object_id][name] = value.__add_reference_json_to__(objects)
                elif isinstance(value, List):
                    values = []
                    for item in value:
                        if isinstance(item, (WorldObject, WorldObject.Reference)):
                            values.append(item.__add_reference_json_to__(objects))
                        else:
                            values.append(item)
                    objects[self.object_id][name] = values
                else:
                    objects[self.object_id][name] = value
        return objects

    ObjectID = _generate_id()


