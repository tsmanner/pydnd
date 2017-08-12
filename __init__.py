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

    char.level_up(Ninja, stats)  # Level 1
    char.level_up(Wizard)  # Level 2
    char.level_up(Ninja)  # Level 3
    stats["wisdom"] += 1
    char.level_up(Wizard, stats)  # Level 4
    char.level_up(Ninja)  # Level 5
    char.level_up(Wizard)  # Level 6
    # char.level_up(Ninja)  # Level 7
    # stats["intelligence"] += 1
    # char.level_up(Wizard, stats)  # Level 8
    # char.level_up(Wizard)  # Level 9
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
