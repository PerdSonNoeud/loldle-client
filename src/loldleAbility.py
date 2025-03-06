import parser
import random as rd

import constants as cons
from champions import Champion
from loldle import Loldle


class LoldleAbility(Loldle):
    def __init__(self):
        super().__init__()
        self.ability = "p"
        self.guesses = []
        self.name = "Nom de la compétence"
        self.rotation = 0
        self.flip = False

    def start(self) -> None:
        super().start()
        self.ability = rd.choice(["p", "q", "w", "e", "r"])
        print(self.champ.abilities)
        self.name = self.champ.abilities[self.ability]
        self.rotation = rd.randint(0, 3)
        self.flip = rd.choice([True, False])

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

    def get_icon(self, filter: bool = False) -> str:
        icon_url = self.champ.get_icon_url(self.ability)
        if not filter:
            return icon_url

        return parser.icon_filter(icon_url, self.rotation, self.flip)
