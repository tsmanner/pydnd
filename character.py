import armor
import classes
import dndtypes
import races
import random
import uuid
import weapons


class CharacterMap(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def add_character(self, character):
        """

        :type character: Character
        """
        self[character.id] = character


characters = CharacterMap()

MALE = "Male"
FEMALE = "Female"


class Character:
    def __init__(self,
                 name, titles, height, weight, looks, race, gender, character_class, class_level, alignment,
                 hit_point_max, initiative, speed, armor_class,
                 attack_bonus,
                 id_num=-1):
        """

        :type name: str
        :type titles: str
        :type height: float
        :type weight: float
        :type looks: str
        :type race: str
        :type gender: str
        :type character_class: str
        :type alignment: str
        :type hit_point_max: int
        :type initiative: int
        :type speed: int
        :type armor_class: int
        :type attack_bonus: int
        """
        # Character Info
        self.name = dndtypes.FullName(name, [dndtypes.Title(title) for title in titles.split("|")])
        self.height = height
        self.weight = weight
        self.looks = looks
        self.race = races.races[race]()
        self.gender = gender
        self.character_class = classes.classes[character_class](class_level)
        self.alignment = dndtypes.alignments[alignment]
        # Stats
        self.hit_point_max = hit_point_max
        self.hit_points = hit_point_max
        self.initiative = initiative
        self.speed = speed
        self.attack_bonus = attack_bonus
        self.armor_class = armor_class
        # Equipment
        self.armor = set()
        self.active_weapon = weapons.Unarmed()
        self.main_hand = self.active_weapon
        self.off_hand = None
        self.secondary_weapon = None
        # Ability Scores
        # Saving Throws
        # Spells
        # Items/Inventory
        self.inventory = []

        # Checks
        self.character_class.check(self)

        # ID information
        if id_num == -1:
            self.id = int(uuid.uuid4())
        else:
            self.id = id_num
        characters.add_character(self)

    def equip(self, item):
        """

        :param item:
        :type item: dndtypes.Equipment
        :return:
        """
        if item in self.inventory:
            if type(item) == weapons.Weapon:
                self.weapons.add(item)

    def roll_initiative(self):
        return self.initiative + random.randint(1, 20)

    def attack(self, enemy):
        """

        :rtype: int, bool, bool, int
        :type enemy: Character
        """
        bonus = self.attack_bonus
        if self.active_weapon:
            bonus += self.active_weapon.attack_bonus
        hit_roll = random.randint(1, 20)
        hit = False
        crit = False
        damage = 0
        # Did we register a hit?
        if hit_roll + bonus >= enemy.armor_class:
            hit = True
            if hit_roll >= self.active_weapon.critical:
                crit_roll = random.randint(1, 20)
                if crit_roll + bonus > enemy.armor_class:
                    crit = True

            # Crit is a bool, so has an int value of 1, so if we crit, we do double damage
            damage = self.active_weapon.damage * (1 + crit)
        # enemy.hit_points -= damage
        return hit_roll, hit, crit, damage

    def __hash__(self):
        return self.id

    def __str__(self):
        return str(self.name) + ": " + str(self.race) + ", " + str(self.character_class)
