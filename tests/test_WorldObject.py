import json
from unittest import TestCase

from world import Location, Passage, WorldObject, to_json


class TestWorldObject(TestCase):
    def test_attrs(self):
        wo = WorldObject()
        wo.name = "foo"
        self.assertIn(("name", "foo"), wo.attrs)

    def test_json(self):
        world = Location(name="The World")
        continent = Location(name="The Continent", location=world)
        kingdom = Location(name="The Kingdom", location=continent)
        city = Location(name="The City", location=kingdom)
        tavern = Location(name="The Tavern", location=city)
        arrival = Passage(location=city, body="Hello World!")

        objects = WorldObject._extract_objects_from_json(json.loads(json.dumps(to_json(world))))
        universe = Location(name="The Universe")
        for root in filter(lambda o: o.location is None, objects.values()):
            universe.add_child_locatable(root)

        # [print(f"{k}: {v} ({v._child_locatables})") for k, v in objects.items()]

        self.assertEqual(1, len(universe._child_locatables))
        self.assertEqual(1, len(objects[1]._child_locatables))
        self.assertEqual(1, len(objects[2]._child_locatables))
        self.assertEqual(1, len(objects[3]._child_locatables))
        self.assertEqual(2, len(objects[4]._child_locatables))
        self.assertEqual(0, len(objects[5]._child_locatables))
        self.assertEqual(0, len(objects[6]._child_locatables))
