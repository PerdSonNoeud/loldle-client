import parser
import random as rd

from .loldleAPI import LoldleAPI


class LoldleAbility(LoldleAPI):
    def __init__(self):
        super().__init__()
        self.ability = "p"
        self.guesses = []
        self.name = "Nom de la compétence"
        self.rotation = 0
        self.flip = False

    def start(self) -> None:
        print("Mode Compétence:")
        super().start()
        self.ability = rd.choice(["p", "q", "w", "e", "r"])
        self.name = self.champ.abilities[self.ability]
        print(f"\t{self.ability}: {self.name}")

        self.rotation = rd.randint(1, 3)
        self.flip = rd.choice([True, False])

    def get_icon(self, filter: bool = False) -> str:
        icon_url = self.champ.get_icon_url(self.ability)
        if not filter:
            return icon_url

        return parser.icon_filter(icon_url, self.rotation, self.flip)
