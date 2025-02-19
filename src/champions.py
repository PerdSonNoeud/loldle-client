import constants as cons


class Champion:
    def __init__(self, data: dict):
        self.name = data["name"]
        self.gender = data["gender"]
        self.positions = data["positions"]
        self.species = data["species"]
        self.resource = data["resource"]
        self.range_type = data["range_type"]
        self.regions = data["regions"]
        self.release = data["release"]
        self.url = cons.get_splash_url(data["name"])

