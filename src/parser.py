import json


def importData(pathfile: str = "assets/champions.json"):
    """
    Function that gets the data from the json file given in argument.

    :param pathfile: Path to the file
    :return: List of dict of the champion
    """
    with open(pathfile) as file:
        return json.load(file)
