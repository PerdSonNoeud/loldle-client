import discord
from discord import app_commands
from discord.ext import commands

import constants as cons


class CogLoldle(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="splash", description="Affiche le splash du champion demander.")
    @app_commands.describe(name="Nom du champion (nom tout collé sans majuscule ex: 'kaisa').")
    async def splash(self, message: discord.Interaction, name: str):
        """
        Function that search the splash art of the champ we're looking for.

        :param message: command of the user
        :param name: name of the champion
        """
        emb = discord.Embed(title=f"{name}", description="Work in progress", color=cons.emb_color)
        emb.set_image(url=cons.get_splash_url(name))
        
        await message.response.send_message(embed=emb, ephemeral=False)

