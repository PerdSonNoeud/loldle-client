import json
import sys

import requests


def loading_bar(iteration, total, length=30):
    percent = iteration / total
    bar = "━" * int(length * percent) + "-" * (length - int(length * percent))
    sys.stdout.write(f"\r[{bar}] {percent * 100:.1f}%")
    sys.stdout.flush()


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
    t_steps = len(result) - 1
    for i in range(t_steps + 1):
        result[i]["skins"] = getSkinId(result[i]["name"])
        loading_bar(i, t_steps)
    print()
    return result


def importFix(pathfile: str = "assets/fixAbility.json"):
    """
    Function that get the data to fix the name of the abilities of certain champions.

    :param pathfile: Path to the file
    :return: List of dict of the fixes
    """
    result = []
    print("Fix ability name...")
    with open(pathfile) as file:
        result = json.load(file)

    return result


def getSkinId(name: str = "Aurelion Sol") -> dict[int:str]:
    """
    Function that import data about skin.
    :param name: name of the champion

    :return: a dictionary with all the skins of the champion
    """
    # Get the last version of league of legends
    version_request = "https://ddragon.leagueoflegends.com/api/versions.json"
    version = requests.get(version_request).json()[0]

    # Get a json version of the data of the champions
    link_requests = "https://ddragon.leagueoflegends.com/cdn/" + version + "/data/fr_FR/championFull.json"

    c_data = requests.get(link_requests).json()["data"]

    # Gether link and info about the skins for each champion
    result = {}
    for v in c_data.values():
        tmp = v["name"].replace("é", "e").replace(" et ", " & ").replace("Maître", "Master")
        if tmp == name:
            for skin in v["skins"]:
                if skin["name"] == "default":
                    result[skin["num"]] = "Par défaut"
                else:
                    result[skin["num"]] = skin["name"]

    return result


url_start = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/"
json_start = "https://raw.communitydragon.org/json/latest/plugins/rcp-be-lol-game-data/global/default/"


def get_splash_url(name: str = "aurelionsol", num: int = 0):
    """
    Function that returns an url link to the splash art.
    :param name: name of the champion we're looking for
    :param skin_id: id of the skin we're looking for

    :return: the url of the splash art
    """
    skin_dir = ""
    if num == 0:
        skin_dir = "base"
    else:
        skin_dir = "skin"
        if num < 10:
            skin_dir += "0" + str(num)
        else:
            skin_dir += str(num)

    if skin_dir == "":
        return "https://salonlfc.com/wp-content/uploads/2018/01/" + "image-not-found-1-scaled-1150x647.png"

    additional = ".mel" if name == "mel" else ""
    return (
        url_start + f"assets/characters/{name}/skins/{skin_dir}/images/{name}_splash_uncentered_{num}{additional}.jpg"
    )


def get_icon_url(name: str = "aurelionsol", icon: str = "base", fixes={}):
    """
    Function that returns an url link to the icon of the champion.
    :param name: name of the champion we're looking for
    :param icon: icon we're looking for (base for champion's icon,
                 "passive" for passive, etc.)

    :return: the url of the icon in a string
    """
    icon_dir = "skins/base/images" if icon == "base" else "hud/icons2d"
    if icon == "base":
        return url_start + f"assets/characters/{name}/{icon_dir}/{name}_splash_tile_0.jpg"

    if fixes != {}:
        return f"{url_start}assets/characters/{name}/{icon_dir}/{fixes[icon]}"

    # Get the complete name of the files
    json = f"{json_start}assets/characters/{name}/{icon_dir}/"
    data = requests.get(json).json()
    for i in range(len(data)):
        if f"{name}_{icon}" in data[i]["name"] or f"{name}{icon}" in data[i]["name"]:
            return f"{url_start}assets/characters/{name}/{icon_dir}/{data[i]["name"]}"
