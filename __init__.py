from functools import partial
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

    gloves_of_dexterity_2 = Equipment("Gloves of Dexterity 2", 4000)
    gloves_of_dexterity_2.dexterity.append(2, "enhancement")
    periapt_of_wisdom_2 = Equipment("Periapt of Wisdom 2", 4000)
    periapt_of_wisdom_2.wisdom.append(2, "enhancement")
    cloak_of_resistance_1 = Equipment("Cloak of Resistance 1", 1000)
    cloak_of_resistance_1.fortitude.append(1, "enhancement")
    cloak_of_resistance_1.reflex.append(1, "enhancement")
    cloak_of_resistance_1.will.append(1, "enhancement")

    char = Character(Halfling)  # Base
    char.armor_class.append(-1, "flaw")  # Flaw: Vulnerable
    char.attack["melee"].append(-2, "flaw")  # Flaw: Noncombatant
    char.equipment.append(gloves_of_dexterity_2)
    char.equipment.append(periapt_of_wisdom_2)
    char.equipment.append(cloak_of_resistance_1)

    point_blank_shot = Feat("Point Blank Shot", "+1 Attack Bonus and Damage with ranged weapons when within 30'")
    precise_shot = Feat("Precise Shot", "No -4 Attack Bonus penalty for shooting into melee.", [point_blank_shot])
    weapon_focus_dart = Feat("Weapon Focus(dart)", "+1 Attack Bonus with darts")
    noncombatant = Flaw("Noncombatant", "-2 on melee Attack Bonus", precise_shot)
    vulnerable = Flaw("Vulnerable", "-1 Armor Class", weapon_focus_dart)
    craven = Feat("Craven", "Add character level to sneak attack damage.")
    fiery_burst = Feat("Fiery Burst", "Nd6 Fire ball, 5' radius, 30' range.", [])
    invisible_needle = Feat("Invisible Needle", "Nd4 force darts as thrown weapons.", [])

    char.level_up(Ninja, stats)  # Level 1
    char.feats[1] = [point_blank_shot]
    char.flaws[1] = [noncombatant, vulnerable]
    char.feats[1].extend([precise_shot, weapon_focus_dart])
    char.level_up(Wizard)  # Level 2
    char.level_up(Ninja)  # Level 3
    char.feats[3] = [craven]
    stats["wisdom"] += 1
    char.level_up(Wizard, stats)  # Level 4
    char.level_up(Ninja)  # Level 5
    char.level_up(Wizard)  # Level 6
    char.feats[6] = [fiery_burst]
    char.level_up(Ninja)  # Level 7
    stats["intelligence"] += 1
    char.level_up(Wizard, stats)  # Level 8
    char.level_up(Wizard)  # partial(Wizard, feat=invisible_needle))  # Level 9
    char.feats[9] = [invisible_needle]
    # char.level_up(MasterThrower)  # Level 10
    # char.level_up(Ninja)  # Level 11
    # stats["intelligence"] += 1
    # char.level_up(Ninja, stats)  # Level 12
    # char.level_up(Wizard)  # Level 13
    # char.level_up(Wizard)  # Level 14
    # char.level_up(Ninja)  # Level 15
    # stats["intelligence"] += 1
    # char.level_up(Wizard, stats)  # Level 16
    # char.level_up(Ninja)  # Level 17
    # char.level_up(Wizard)  # Level 18
    # char.level_up(Ninja)  # Level 19
    # stats["intelligence"] += 1
    # char.level_up(Wizard, stats)  # Level 20

    print(char.__str__(verbose=True))
