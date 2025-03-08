import constants as cons
from champions import Champion
from loldle import Loldle


def compareOne(data1: str, data2: str):
    return cons.good if data1 == data2 else cons.wrong


def compareMultiple(data1: list[str], data2: list[str]):
    n = sum(p in data1 for p in data2)

    if len(data1) == 1 and len(data2) == 1:
        return cons.good if data1 == data2 else cons.wrong
    if n == len(data1) == len(data2):
        return cons.good
    elif n > 0:
        return cons.partial
    return cons.wrong


class LoldleClassic(Loldle):
    def __init__(self):
        super().__init__()

    def start(self):
        print("Mode Classique:")
        super().start()

    def guess(self, guess: Champion) -> bool:
        # Champion
        icon = cons.random
        # Gender
        gen = compareOne(self.champ.gender, guess.gender)
        # Species
        spe = compareMultiple(self.champ.species, guess.species)
        # Position
        pos = compareMultiple(self.champ.positions, guess.positions)
        # Resources
        res = compareOne(self.champ.resource, guess.resource)
        # Range type
        ran = compareMultiple(self.champ.range_type, guess.range_type)
        # Regions
        reg = compareMultiple(self.champ.regions, guess.regions)
        # Release Year
        if self.champ.release > guess.release:
            rel = cons.higher
        elif self.champ.release < guess.release:
            rel = cons.lower
        else:
            rel = cons.good

        # Add the result to the list
        self.guesses.insert(0, [icon, gen, spe, pos, res, ran, reg, rel, guess.name])
        return gen == spe == pos == res == ran == reg == rel == cons.good
