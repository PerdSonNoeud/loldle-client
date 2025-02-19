emb_color = 0xff0000

lol_version = "14.22.1"

good = "🟩"
partial = "🟧"
wrong = "🟥"
higher = "⬆️"
lower = "⬇️"

random = "❔"


def get_splash_url(name: str = "aurelionsol", skin_id: str = "base"):
    """
    Function that returns an url link to the splash art.
    :param name: name of the champion we're looking for
    :param skin_id: id of the skin we're looking for

    :return: the url of the splash art
    """
    url_start = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/"
    return (
        url_start
        + f"assets/characters/{name}/skins/{skin_id}/images/{name}_splash_uncentered_0.jpg"
    )

