import discord
from discord import app_commands
from discord.ext import commands

import constants as cons
from loldle import Loldle


class CogLoldle(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.loldle = Loldle()
        self.isPlaying = False

    @app_commands.command(name="splash", description="Affiche le splash du champion demander.")
    @app_commands.describe(name="Nom du champion (nom tout collé sans majuscule ex: 'kaisa').")
    async def splash(self, message: discord.Interaction, name: str):
        """
        Function that search the splash art of the champ we're looking for.

        :param message: Command of the user
        :param name: Name of the champion
        """
        emb = discord.Embed(title=f"{name}", description="Work in progress", color=cons.emb_color)
        emb.set_image(url=cons.get_splash_url(name))
        
        await message.response.send_message(embed=emb, ephemeral=False)

    @app_commands.command(name="start", description="Commence une partie de Loldle.")
    async def start(self, message: discord.Interaction):
        """
        Function that start a new game.

        :param message: Command of the user
        """
        if self.isPlaying:
            text = "Une partie est encore en cours !"
            eph = True
        else:
            self.isPlaying = True
            self.loldle.start()
            text =  "Nouvelle partie commencée !"
            eph = False
        await message.response.send_message(content=text, ephemeral=eph)
