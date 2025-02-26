import discord
from discord import app_commands

import constants as cons
from cogLoldle import CogLoldle


class CogLoldleOther(CogLoldle):
    def __init__(self, client):
        super().__init__(client)

    @app_commands.command(
        name="splash", description="Afficher le skin du champion demandé."
    )
    @app_commands.describe(
        champion="Nom du champion.",
        skin="Nom du skin du champion."
    )
    @app_commands.autocomplete(
        champion=CogLoldle.autocomplete,
        skin=CogLoldle.autocomplete_skin
    )
    async def splash(self, message: discord.Interaction,
                     champion: str, skin: int = 0):
        """
        Function that search the splash art of the champ we're looking for.

        :param message: Command of the user
        :param name: Name of the champion
        """
        emb = discord.Embed(
            title=f"{champion}", description="Work in progress",
            color=cons.emb_color
        )
        emb.set_image(url=cons.get_splash_url(champion, skin))

        await message.response.send_message(embed=emb, ephemeral=False)
