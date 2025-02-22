import random as rd

import constants as cons
from champions import Champion


def compareOne(data1: str, data2: str):
    return cons.good if data1 == data2 else cons.wrong

def compareMultiple(data1: list[str], data2: list[str]):
    n = sum(p in data1 for p in data2)

    if len(data1) == 1 and len(data2) == 1:
            return cons.good if data1 == data2 else cons.wrong

    return cons.good if n == len(data1) == len(data2) else cons.partial if n > 0 else cons.wrong

class LoldleClassic:
    def __init__(self):
        self.champ = None
        self.guesses = []

    def start(self):
        """
        Function that start the classic mode of loldle.
        It initialise the base value of the champion to guess (random between 
        all of them) and reset the number of tries (clear the history of guesses).
        """
        champ_dict = rd.choice(Champion.champ_list)
        print("Champion aléatoire:", champ_dict)
        self.champ = Champion(champ_dict)
        self.guesses = []

    def guess(self, guess: Champion):
        # Champion
        # TODO: return the champ icon
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

    def __str__(self):
        result = f"Nombre total d'essais : {len(self.guesses)}\n"
        for i in range(len(self.guesses)):
            if i >= 10:
                return result
            for info in self.guesses[i]:
                result += info + " "
            result += "\n"
        return result

