import random as rd

import constants as cons
from champions import Champion
from loldle import Loldle


class LoldleAbility(Loldle):
    def __init__(self):
        super().__init__()
        self.ability = "p"
        self.guesses = []

    def start(self) -> None:
        super().start()
        self.ability = rd.choice(["p", "q", "w", "e", "r"])

    def guess(self, champ: Champion):
        """
        Function that checks if the champ is the right one
        """
        if self.champ.name == champ.name:
            self.guesses.insert(0, [cons.good, champ.name])
            return True
        else:
            self.guesses.insert(0, [cons.wrong, champ.name])
            return False

    def get_icon(self):
        return self.champ.getIcon(self.ability)
