import random as rd

import constants as cons
from champions import Champion, initChamp


class Loldle:
    def __init__(self):
        self.champ = None
        self.guesses = []
        
        # Initialize champions
        initChamp()

    def start(self):
        # TODO: Import a random dict from a database
        champ_dict = {
            "name": "Aurelion Sol",
            "alias": "aurelionsol",
            "gender": "Male",
            "positions": ["Mid"],
            "species": ["Celestial", "Dragon"],
            "resource": "Mana",
            "range_type": ["ranged"],
            "regions": ["Runeterra", "Targon"],
            "release": 2016
        }
        self.champ = Champion(champ_dict)
        self.guesses = []
        pass

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
        resource = cons.green if self.champ.resource == guess.resource else cons.wrong

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
        elif self.champ.release < gess.release:
            release = cons.lower
        else:
            release = cons.good

        # Return the result
        return [icon, gender, positions, resource, range_type, regions, release]

    def __str__(self):
        result = ""
        for guess in self.guesses:
            for icon in guess:
                result += icon + " "
            result += "\n"
        return result
