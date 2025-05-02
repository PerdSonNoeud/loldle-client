import discord
from discord.ext import commands

import champions


class CogLoldle(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Autocompletion for guess command
    async def autocomplete(self, message: discord.Interaction, current: str):
        champ = [(ch["name"], ch["alias"]) for ch in champions.Champion.champ_list]

        # Not searching
        if not current:
            return [discord.app_commands.Choice(name=ch[0], value=ch[1]) for ch in champ[:25]]

        # Sorting priority: starts with > contains
        starts_with = [ch for ch in champ if ch[0].lower().startswith(current.lower())]
        contains = [ch for ch in champ if current.lower() in ch[0].lower() and ch not in starts_with]

        results = starts_with + contains  # Merge lists with priority
        return [discord.app_commands.Choice(name=ch[0], value=ch[1]) for ch in results[:25]]

    # Autocompletion for skin
    async def autocomplete_skin(self, message: discord.Interaction, current: str):
        champ_list = champions.Champion.champ_list
        champ = [ch["alias"] for ch in champ_list]

        champion = message.namespace.champion

        if champion in champ:
            i = champ.index(champion)
            tmp = champ_list[i]["skins"]
            skins = [(tmp[k]["name"], tmp[k]["num"]) for k in range(len(tmp))]
            # Not searching
            if not current:
                return [discord.app_commands.Choice(name=skin[0], value=skin[1]) for skin in skins[:25]]

            # Sorting priority: starts with > contains
            starts_with = [skin for skin in skins if skin[0].lower().startswith(current.lower())]
            contains = [skin for skin in skins if current.lower() in skin[0].lower() and skin not in starts_with]

            results = starts_with + contains  # Merge lists with priority
            return [discord.app_commands.Choice(name=skin[0], value=skin[1]) for skin in results[:25]]

        return []
