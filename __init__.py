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
    char.level_up(Wizard)
    char.levels[0].feats = [point_blank_shot]
    char.level_up(Wizard)
    char.levels[1].feats = [weapon_focus("dart")]
    [print(item) for item in char.levels[1]._aspects()]


    # char.equipment.append(gloves_of_dexterity(2))
    # char.equipment.append(periapt_of_wisdom(2))
    # char.equipment.append(cloak_of_resistance(1))
    # char.equipment.append(ring_of_ua_reduce_person_1_str)

    """ Level 1 """
    # char.level_up(Ninja, stats)
    # char.feats[1] = [point_blank_shot]
    # char.flaws = [noncombatant(precise_shot), vulnerable(weapon_focus("dart"))]
    # char.feats[1].extend([precise_shot, weapon_focus("dart")])

    # print(char.__str__(verbose=True))
