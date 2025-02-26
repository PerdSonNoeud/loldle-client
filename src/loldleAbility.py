import random as rd

from loldle import Loldle


class LoldleAbility(Loldle):
    def __init__(self):
        super().__init__()
        self.ability = "passive"

    def random_ability(self):
        self.ability = rd.choice(["passive", "q", "w", "e", "r"])

    def guess(self, champ: list[str]):
        """
        Function that checks if the champ is the right one
        """
        return self.champ.name == champ["name"]
