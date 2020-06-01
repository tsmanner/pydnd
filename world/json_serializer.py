import collections
import re
from typing import List, Set
import world


def to_json(*objs):
    objects = {}
    [add_json_to_dict(obj, objects) for obj in objs]
    return collections.OrderedDict({k: objects[k] for k in sorted(objects)})


def _to_json(obj, objects: dict):
    if isinstance(obj, List):
        return [_to_json(item, objects) for item in obj]
    elif isinstance(obj, world.WorldObject):
        add_json_to_dict(obj, objects)
        return f"<<{obj.object_id}>>"
    else:
        return obj


def add_json_to_dict(world_object: world.WorldObject, objects: dict):
    if world_object.object_id not in objects:
        objects[world_object.object_id] = {
            "object_type": type(world_object).__name__
        }
        for attribute_name, attribute_value in world_object.attrs:
            objects[world_object.object_id][attribute_name] = _to_json(attribute_value, objects)


def from_json(json_dict: dict):
    objects = {}
    for object_id, object_data in json_dict.items():
        new_object = getattr(world, object_data.pop("object_type"))(object_id=int(object_id))
        for attribute_name, attribute_value in object_data.items():
            setattr(new_object, attribute_name, attribute_value)
        objects[int(object_id)] = new_object

    for new_object in objects.values():
        for attribute_name, attribute_value in new_object.attrs:
            if isinstance(attribute_value, List):
                resolved_value = []
                for item in attribute_value:
                    if isinstance(item, str):
                        match = re.match(r"<<(?P<object_id>-?\d+)>>", item)
                        if match:
                            resolved_value.append(objects[int(match["object_id"])])
                        else:
                            resolved_value.append(item)
                    else:
                        resolved_value.append(item)
                setattr(new_object, attribute_name, resolved_value)
            elif isinstance(attribute_value, str):
                match = re.match(r"<<(?P<object_id>-?\d+)>>", attribute_value)
                if match:
                    setattr(new_object, attribute_name, objects[int(match["object_id"])])
                else:
                    setattr(new_object, attribute_name, attribute_value)
            else:
                setattr(new_object, attribute_name, attribute_value)
    return objects
