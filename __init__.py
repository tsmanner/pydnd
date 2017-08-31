from app import *

if __name__ == '__main__':
    stats = {
        "strength": 13,
        "dexterity": 16,
        "constitution": 10,
        "intelligence": 12,
        "wisdom": 17,
        "charisma": 6,
    }

    char = Character(Halfling)  # Base
    char.equipment.append(gloves_of_dexterity(2))
    char.equipment.append(periapt_of_wisdom(2))
    char.equipment.append(cloak_of_resistance(1))

    """ Level 1 """
    char.level_up(Ninja, stats)
    char.feats[1] = [point_blank_shot]
    char.flaws = [noncombatant(precise_shot), vulnerable(weapon_focus("dart"))]
    char.feats[1].extend([precise_shot, weapon_focus("dart")])
    """ Level 2 """
    char.level_up(Wizard)
    """ Level 3 """
    char.level_up(Ninja)
    char.feats[3] = [craven]
    """ Level 4 """
    stats["wisdom"] += 1
    char.level_up(Wizard, stats)
    """ Level 5 """
    char.level_up(Ninja)
    """ Level 6 """
    char.level_up(Wizard)
    char.feats[6] = [fiery_burst]
    """ Level 7 """
    char.level_up(Ninja)
    """ Level 8 """
    stats["intelligence"] += 1
    char.level_up(Wizard, stats)
    """ Level 9 """
    char.level_up(Wizard)  # partial(Wizard, feat=invisible_needle))
    char.feats[9] = [invisible_needle]
    """ Level 10 """
    # char.level_up(MasterThrower)  # Level 10
    """ Level 11 """
    # char.level_up(Ninja)  # Level 11
    """ Level 12 """
    # stats["intelligence"] += 1
    # char.level_up(Ninja, stats)  # Level 12
    # char.feats[12]
    """ Level 13 """
    # char.level_up(Wizard)  # Level 13
    """ Level 14 """
    # char.level_up(Wizard)  # Level 14
    """ Level 15 """
    # char.level_up(Ninja)  # Level 15
    """ Level 16 """
    # stats["intelligence"] += 1
    # char.level_up(Wizard, stats)  # Level 16
    """ Level 17 """
    # char.level_up(Ninja)  # Level 17
    """ Level 18 """
    # char.level_up(Wizard)  # Level 18
    """ Level 19 """
    # char.level_up(Ninja)  # Level 19
    """ Level 20 """
    # stats["intelligence"] += 1
    # char.level_up(Wizard, stats)  # Level 20

    print(char.__str__(verbose=True))
