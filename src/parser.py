import json

import requests


def importData(pathfile: str = "assets/champions.json"):
    """
    Function that gets the data from the json file given in argument.

    :param pathfile: Path to the file
    :return: List of dict of the champion
    """
    result = []
    with open(pathfile) as file:
        result = json.load(file)

    print("Importing skins...")
    for i in range(len(result)):
        result[i]["skins"] = getSkinId(result[i]["name"])
        print(result[i]["name"], len(result[i]["skins"]))
    return result


def getSkinId(name: str = "Aurelion Sol") -> dict[int:str]:
    """
    Function that import data about skin.
    """
    # Get the last version of league of legends
    version_request = "https://ddragon.leagueoflegends.com/api/versions.json"
    version = requests.get(version_request).json()[0]

    # Get a json version of the data of the champions
    link_requests = (
        "https://ddragon.leagueoflegends.com/cdn/"
        + version
        + "/data/fr_FR/championFull.json"
    )

    c_data = requests.get(link_requests).json()["data"]

    # Gether link and info about the skins for each champion
    result = {}
    for v in c_data.values():
        if v["name"] == name:
            for skin in v["skins"]:
                if skin["name"] == "default":
                    result[skin["num"]] = "Par défaut"
                else:
                    result[skin["num"]] = skin["name"]

    return result
