import pandas as pd

import app.base


def character():
    levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    proficiency = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6]
    return pd.DataFrame(data={"proficiency": proficiency},
                        index=levels)


def rogue():
    levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    sneak_dice = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]
    features = [
        ["Expertise", "Sneak Attack", "Thieves' Cant"],
        ["Cunning Action"],
        [],
        ["Ability Score"],
        ["Uncanny Dodge"],
        ["Expertise"],
        ["Evasion"],
        ["Ability Score"],
        [],
        ["Ability Score"],
        ["Reliable Talent"],
        ["Ability Score"],
        [],
        ["Blindsense"],
        ["Slippery Mind"],
        ["Ability Score"],
        [],
        ["Elusive"],
        ["Ability Score"],
        ["Stroke of Luck"],
    ]
    return pd.DataFrame(data={"sneak_dice": sneak_dice,
                              "features": features},
                        index=levels)


def arcane_trickster():
    levels = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    cantrips = [3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    spells_known = [3, 4, 4, 4, 5, 6, 6, 7, 8, 8, 9, 10, 10, 11, 11, 11, 12, 13]
    slots_1 = [2, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    slots_2 = [None, None, None, None, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    slots_3 = [None, None, None, None, None, None, None, None, None, None, 2, 2, 2, 3, 3, 3, 3, 3]
    slots_4 = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 1]
    features = [
        ["Mage Hand Legerdemain"],
        [],
        [],
        [],
        [],
        [],
        ["Magical Ambusher"],
        [],
        [],
        [],
        ["Versatile Trickster"],
        [],
        [],
        [],
        ["Spell Thief"],
        [],
        [],
        [],
    ]
    return pd.DataFrame(data={"cantrips": cantrips,
                              "spells_known": spells_known,
                              "slots_1": slots_1,
                              "slots_2": slots_2,
                              "slots_3": slots_3,
                              "slots_4": slots_4,
                              "features": features},
                        index=levels)


if __name__ == '__main__':
    c = character()
    r = rogue()
    at = arcane_trickster()
    char = app.base.merge(c, r, at)
    print(char)
    # for level in char.index:
    #     row = char.loc[level]
    #     print(level, " ".join([str(row[col]) for col in char.columns]))
