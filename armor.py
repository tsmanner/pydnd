import dndtypes


class Armor(dndtypes.Equipment):
    def __init__(self, armor_bonus, max_dex_bonus, armor_check_penalty, spell_fail_chance, weight):
        dndtypes.Item.__init__(self)
        self.armor_bonus = armor_bonus
        self.max_dex = max_dex_bonus
        self.armor_check_penalty = armor_check_penalty
        self.spell_fail_chance = spell_fail_chance
        self.weight = weight


class Shield(Armor):
    def __init__(self):
        Armor.__init__(self)


class LeatherArmor(Armor):
    def __init__(self):
        Armor.__init__(self,
                       armor_bonus=2,
                       max_dex_bonus=6,
                       armor_check_penalty=0,
                       spell_fail_chance=10,
                       weight=15)
