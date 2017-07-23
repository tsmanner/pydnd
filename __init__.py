from app import *

if __name__ == '__main__':
    char = Character(Halfling)
    """ Level 1 """
    char.abilities[1] = Abilities(13, 16, 10, 12, 17, 6)
    char.level_up(Ninja)
    """ Level 2 """
    char.level_up(Wizard)
    """ Level 3 """
    char.level_up(Ninja)
    """ Level 4 """
    char.abilities[1] = Abilities(wisom=1)
    char.level_up(Wizard)
    """ Level 5 """
    char.level_up(Ninja)
    """ Level 6 """
    char.level_up(Wizard)
    """ Level 7 """
    char.level_up(Ninja)
    """ Level 8 """
    char.level_up(Wizard)
    """ Level 9 """
    char.level_up(Wizard)
    """ Level 10 """
    char.level_up(Ninja)
    """ Level 11 """
    char.level_up(Wizard)
    """ Level 12 """
    char.level_up(Ninja)
    """ Level 13 """
    char.level_up(Wizard)
    """ Level 14 """
    char.level_up(Ninja)
    print(char)
    print(char.hit_die(5).roll)
