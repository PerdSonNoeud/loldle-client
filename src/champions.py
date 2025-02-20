import constants as cons


def initChamp():
    # TODO: Import file from json file
    pass


def getChamp(name: str):
    for champ in Champion.champ_list:
        if name == champ["name"] or name == champ["alias"]:
            return champ
    return None


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

    def getUrl(self):
        return cons.get_splash_url(data["alias"])

    def getIcon(self):
        return cons.get_icon_url(data["alias"])

