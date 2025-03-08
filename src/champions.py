import parser
import random as rd


def initChamp():
    return parser.importData()


def getChamp(name: str):
    for champ in Champion.champ_list:
        if name == champ["name"] or name == champ["alias"]:
            return Champion(champ)
    return None


def rdChamp():
    return rd.choice(Champion.champ_list)
    # return Champion.champ_list[-5]


class Champion:
    champ_list = initChamp()
    icon_fix = parser.importFix()

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
        self.abilities = data["abilities"]

    def getUrl(self, num: int = str):
        return parser.get_splash_url(self.alias, 0)

    def get_icon_url(self, ability: str = "base"):
        fix = {}
        for data in Champion.icon_fix:
            if data["name"] == self.alias:
                fix = data
                break
        return parser.get_icon_url(self.alias, ability, fix)
