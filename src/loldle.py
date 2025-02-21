import random as rd

import constants as cons
from champions import Champion


class Loldle:
    def __init__(self):
        self.champ = None
        self.guesses = []

    def start(self):
        champ_dict = rd.choice(Champion.champ_list)
        print("Champion aléatoire:", champ_dict)
        self.champ = Champion(champ_dict)
        self.guesses = []

    def guess(self, guess: Champion):
        # Champion
        # TODO: return the champ icon
        icon = cons.random

        # Gender
        gender = cons.good if self.champ.gender == guess.gender else cons.wrong

        # Position
        n = 0
        for pos in guess.positions:
            if pos in self.champ.positions:
                n += 1
        if n == 0:
            positions = cons.wrong
        elif n < len(self.champ.positions):
            positions = cons.partial
        else:
            positions = cons.good

        # Species
        n = 0
        for spe in guess.species:
            if spe in self.champ.species:
                n += 1
        if n == 0:
            species = cons.wrong
        elif n < len(self.champ.species):
            species = cons.partial
        else:
            species = cons.good

        # Resources
        resource = cons.good if self.champ.resource == guess.resource else cons.wrong

        # Range type
        n = 0
        for r_type in guess.range_type:
            if r_type in self.champ.range_type:
                n += 1
        if n == 0:
            range_type = cons.wrong
        if n < len(self.champ.range_type):
            range_type = cons.partial
        else:
            range_type = cons.good

        # Regions
        n = 0
        for reg in guess.regions:
            if reg in self.champ.regions:
                n += 1
        if n == 0:
            regions = cons.wrong
        elif n < len(self.champ.regions):
            regions = cons.partial
        else:
            regions = cons.good

        # Release Year
        if self.champ.release > guess.release:
            release = cons.higher
        elif self.champ.release < guess.release:
            release = cons.lower
        else:
            release = cons.good

        # Add the result to the list
        self.guesses.insert(0, [icon, gender, species, positions, resource, range_type, regions, release])
        return gender == species == positions == resource == range_type == regions == release == cons.good

    def __str__(self):
        result = ""
        for guess in self.guesses:
            for icon in guess:
                result += icon + " "
            result += "\n"
        return result
