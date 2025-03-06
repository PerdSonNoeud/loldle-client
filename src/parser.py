import json
import sys
from io import BytesIO

import requests
from PIL import Image


def loading_bar(iteration, total, length=30):
    """
    function that create loading bar in the console.
    Might need it later
    """
    percent = iteration / total
    bar = "━" * int(length * percent) + "-" * (length - int(length * percent))
    sys.stdout.write(f"\r[{bar}] {percent * 100:.1f}%")
    sys.stdout.flush()


def get_version() -> str:
    """
    Function that get the last version of league of legends.
    """
    version_request = "https://ddragon.leagueoflegends.com/api/versions.json"
    return requests.get(version_request).json()[0]


def importData(pathfile: str = "assets/champions.json") -> list[dict]:
    """
    Function that gets the data from the json file given in argument.

    :param pathfile: Path to the file
    :return: List of dict of the champion
    """
    result = []
    print("Get champions data...")
    with open(pathfile) as file:
        result = json.load(file)

    # Get a json version of the data of the champions
    link_requests = f"https://ddragon.leagueoflegends.com/cdn/{get_version()}/data/fr_FR/championFull.json"
    c_data = requests.get(link_requests).json()["data"]

    print("Importing skins and abilities...")
    # Link data to champ
    data = list(c_data.values())

    abilities = ["q", "w", "e", "r"]

    for i in range(len(data)):
        # Get skin's name
        for skin in data[i]["skins"]:
            if skin["name"] == "default":
                skin["name"] = "Par défaut"
                break
        result[i]["skins"] = data[i]["skins"]
        # Get abilities name
        result[i]["abilities"] = {"p": data[i]["passive"]["name"]}
        tmp = list(data[i]["spells"])
        for j in range(len(tmp)):
            result[i]["abilities"][abilities[j]] = tmp[j]["name"].split("/")[0]
    return result


def importFix(pathfile: str = "assets/fixAbility.json"):
    """
    Function that get the data to fix the name of the abilities of certain champions.

    :param pathfile: Path to the file
    :return: List of dict of the fixes
    """
    result = []
    print("Fix abilities image name...")
    with open(pathfile) as file:
        result = json.load(file)

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
        return "https://salonlfc.com/wp-content/uploads/2018/01/image-not-found-1-scaled-1150x647.png"

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
        if (
            f"{name}_{icon}" in data[i]["name"]
            or f"{name}{icon}" in data[i]["name"]
            or f"{name}_icon_{icon}" in data[i]["name"]
        ):
            return f"{url_start}assets/characters/{name}/{icon_dir}/{data[i]['name']}"


def icon_filter(url: str, rotation: int = 0, flip: bool = False):
    response = requests.get(url)
    if response.status_code != 200:
        return url

    image = Image.open(BytesIO(response.content))
    image = image.convert("L")
    if flip:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    image = image.rotate(90 * rotation)
    return image
