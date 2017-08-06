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
    char.wisdom.append(2, "enhancement")  # Periapt of Wisdom
    char.dexterity.append(2, "enhancement")  # Gloves of Dexterity

    char.level_up(Ninja, stats)  # Level 1
    char.level_up(Wizard)  # Level 2
    char.level_up(Ninja)  # Level 3
    stats["wisdom"] += 1
    char.level_up(Wizard, stats)  # Level 4
    char.level_up(Ninja)  # Level 5
    char.level_up(Wizard)  # Level 6
    char.level_up(Ninja)  # Level 7
    stats["intelligence"] += 1
    char.level_up(Wizard, stats)  # Level 8
    char.level_up(Wizard)  # Level 9
    char.level_up(MasterThrower)  # Level 10
    char.level_up(Ninja)  # Level 11
    stats["intelligence"] += 1
    char.level_up(Ninja)  # Level 12

    print(char)
