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

    char = Character(Halfling)  # Base
    char.armor_class.append(-1, "flaw")  # Flaw: Vulnerable
    char.attack["melee"].append(-2, "flaw")  # Flaw: Noncombatant
    char.dexterity.append(2, "enhancement")  # +2 Gloves of Dexterity
    char.wisdom.append(2, "enhancement")  # +2 Periapt of Wisdom
    char.fortitude.append(1, "enhancement")  # +1 Cloak of Resistance
    char.reflex.append(1, "enhancement")  # +1 Cloak of Resistance
    char.will.append(1, "enhancement")  # +1 Cloak of Resistance

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

    print(char.__str__(True))
