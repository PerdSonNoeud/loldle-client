import parser
import random as rd

import constants as cons


def initChamp():
    return parser.importData()


def getChamp(name: str):
    for champ in Champion.champ_list:
        if name == champ["name"] or name == champ["alias"]:
            return Champion(champ)
    return None


def rdChamp():
    return rd.choice(Champion.champ_list)


class Champion:
    champ_list = initChamp()

    def __init__(self, data: dict):
        self.name = data["name"]
        self.alias = data["alias"]
        self.gender = data["gender"]
        self.positions = data["positions"]
        self.species = data["species"]
        self.resource = data["resource"]
        self.range_type = data["range_type"]
        self.regions = data["regions"]
        self.release = data["release"]
        self.skins = data["skins"]

    def getUrl(self, num: int = str):
        return cons.get_splash_url(self.alias, 0)

    def getIcon(self):
        return cons.get_icon_url(self.alias)
