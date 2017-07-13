import uuid


class ItemMap(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def add_item(self, item):
        """

        :type item: Item
        """
        self[item.id] = item

item_map = ItemMap()


class Spell:
    def __init__(self, name, cast_time, cast_range, effect, duration, saving_throw, spell_resistance, level):
        self.name = name
        self.cast_time = cast_time
        self.cast_range = cast_range
        self.effect = effect
        self.duration = duration
        self.saving_throw = saving_throw
        self.spell_resistance = spell_resistance
        self.level = level


class Item:
    def __init__(self, id_num):
        if id_num == -1:
            self.id = uuid.uuid4()
        else:
            self.id = id_num
        item_map.add_item(self)

    def __hash__(self):
        return self.id


class Equipment(Item):
    def __init__(self, id_num):
        Item.__init__(self, id_num=id_num)
        self.equipped = False


class Title:
    def __init__(self, title, after=False):
        self.title = title
        self.after = after

    def add_title(self, name):
        if self.after:
            return name + ', ' + self.title
        return self.title + ' ' + name


class FullName:
    def __init__(self, name, titles):
        self.name = name
        self.titles = titles
        if len(titles):
            self.active_title = titles[0]
        else:
            self.active_title = None

    def select_title(self, idx):
        if idx >= len(self.titles):
            raise IndexError()
        self.active_title = self.titles[idx]

    def __str__(self):
        if self.active_title:
            return self.active_title.add_title(self.name)
        return self.name


class Alignment:
    """
    Alignment Values
    """
    class Neutral:
        def __str__(self):
            return "Neutral"

        def __int__(self):
            return 1

    class Lawful:
        def __str__(self):
            return "Lawful"

        def __int__(self):
            return 0

    class Chaotic:
        def __str__(self):
            return "Chaotic"

        def __int__(self):
            return 2

    class Good:
        def __str__(self):
            return "Good"

        def __int__(self):
            return 0

    class Evil:
        def __str__(self):
            return "Evil"

        def __int__(self):
            return 2

    NEUTRAL = Neutral()
    LAWFUL = Lawful()
    CHAOTIC = Chaotic()
    GOOD = Good()
    EVIL = Evil()

    def __init__(self, ethics, morality):
        # Lawful, Neutral, Chaotic
        self.ethics = ethics
        # Good, Neutral, Evil
        self.morality = morality

    def __eq__(self, other):
        """

        :type other: Alignment
        :return:
        """
        return self.ethics is other.ethics and self.morality is other.morality

    def __hash__(self):
        return int(self.ethics) + 3*int(self.morality)

    def __str__(self):
        if self.ethics == self.morality == Alignment.NEUTRAL:
            return str(self.ethics)
        return str(self.ethics) + " " + str(self.morality)

    def __repr__(self):
        return str(self)

alignments = {"Lawful Good": Alignment(Alignment.LAWFUL, Alignment.GOOD),
              "Lawful Neutral": Alignment(Alignment.LAWFUL, Alignment.NEUTRAL),
              "Lawful Evil": Alignment(Alignment.LAWFUL, Alignment.EVIL),
              "Neutral Good": Alignment(Alignment.NEUTRAL, Alignment.GOOD),
              "Neutral": Alignment(Alignment.NEUTRAL, Alignment.NEUTRAL),
              "Neutral Evil": Alignment(Alignment.NEUTRAL, Alignment.EVIL),
              "Chaotic Good": Alignment(Alignment.CHAOTIC, Alignment.GOOD),
              "Chaotic Neutral": Alignment(Alignment.CHAOTIC, Alignment.NEUTRAL),
              "Chaotic Evil": Alignment(Alignment.CHAOTIC, Alignment.EVIL)}


class BadAlignmentError(ValueError):
    def __init__(self, *args, **kwargs):
        ValueError.__init__(self, *args, **kwargs)
