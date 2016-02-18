import dndtypes
import character

SMALL = 0
MEDIUM = 1
LARGE = 2


class CharacterClass:
    def __init__(self, name, level):
        self.name = name
        self.level = level

    def check(self, char):
        pass

    def __str__(self):
        return "Level " + str(self.level) + " " + self.name


class Druid(CharacterClass):
    def __init__(self, level):
        CharacterClass.__init__(self, name="Druid", level=level)
        self.legal_alignments = {dndtypes.alignments['Neutral Good'],
                                 dndtypes.alignments['Neutral'],
                                 dndtypes.alignments['Neutral Evil'],
                                 dndtypes.alignments['Lawful Neutral'],
                                 dndtypes.alignments['Chaotic Neutral']}

    def check(self, char):
        """

        :type  char: character.Character
        """
        if char.alignment not in self.legal_alignments:
            raise dndtypes.BadAlignmentError("Illegal alignment for Druid: " +
                                             str(char.alignment) +
                                             ". Must be neutral on one axis.")


class Warrior(CharacterClass):
    def __init__(self, level):
        CharacterClass.__init__(self, name="Warrior", level=level)


classes = {"Druid": Druid,
           "Warrior": Warrior}
