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

    def getUrl(self, skin: str = "Par défaut"):
        skin_dir = ""
        if skin == "Par défaut":
            skin_dir = "base"
            skin_id = 0
        else:
            for k, v in self.skins.items():
                if skin == v:
                    skin_dir = "skin"
                    skin_id = int(k)
                    if v < 10:
                        skin_dir += "0" + v
                    else:
                        skin_dir += v
                    break

        if skin_dir == "":
            return (
                "https://salonlfc.com/wp-content/uploads/2018/01/"
                + "image-not-found-1-scaled-1150x647.png"
            )

        return cons.get_splash_url(self.alias, skin_dir, skin_id)

    def getIcon(self):
        return cons.get_icon_url(self.alias)
