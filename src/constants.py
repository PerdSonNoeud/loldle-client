emb_color = 0xff0000


good = "🟩"
partial = "🟧"
wrong = "🟥"
higher = "⬆️"
lower = "⬇️"

random = "❔"


url_start = (
    "https://raw.communitydragon.org/latest/plugins/" +
    "rcp-be-lol-game-data/global/default/"
)


def get_splash_url(name: str = "aurelionsol",
                   skin_id: str = "base", num: int = 0):
    """
    Function that returns an url link to the splash art.
    :param name: name of the champion we're looking for
    :param skin_id: id of the skin we're looking for

    :return: the url of the splash art
    """
    additional = ".mel" if name == "mel" else ""
    return (
        url_start +
        f"assets/characters/{name}/skins/{skin_id}/" +
        f"images/{name}_splash_uncentered_{num}{additional}.jpg"
    )


def get_icon_url(name: str = "aurelionsol", icon: str = "base"):
    """
    Function that returns an url link to the icon of the champion.
    :param name: name of the champion we're looking for
    :param icon: icon we're looking for (base for champion's icon,
                 "passive" for passive, etc.)

    :return: the url of the icon in a string
    """
    icon_dir = "skins/base/images" if icon == "base" else "hud/icon2d"
    if icon == "base":
        return (
            url_start +
            f"assets/characters/{name}/{icon_dir}/{name}_splash_tile_0.jpg"
        )

    return (
        url_start +
        f"assets/characters/{name}/{icon_dir}/{name}_{icon}.png"
    )
