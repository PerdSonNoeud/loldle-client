import parser
import random as rd

from .loldleAPI import LoldleAPI


class LoldleSplash(LoldleAPI):
    def __init__(self):
        super().__init__()
        self.skinID = 0
        self.name = "Nom du skin"
        self.pos_factor = [0, 0]

    def start(self) -> None:
        print("Mode Splash:")
        super().start()
        self.pos_factor = [rd.randint(0, 65) / 100, rd.randint(0, 50) / 100]
        self.skinID = rd.randint(0, len(self.champ.skins) - 1)
        self.name = self.champ.skins[self.skinID]["name"]
        print(f"\tSkin: {self.name}")

    def get_splash(self, filter: bool = False) -> str:
        splash_url = self.champ.get_url(self.champ.skins[self.skinID]["num"])
        if not filter:
            return splash_url
        return parser.splash_filter(splash_url, self.pos_factor)
