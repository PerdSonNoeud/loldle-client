import discord
from discord import app_commands
from discord.ext import commands

import champions
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

    @app_commands.command(name="guess", description="Deviner un champion.")
    @app_commands.describe(name="Nom du champion à deviner.")
    async def guess(self, message: discord.Interaction, name: str):
        """
        Function that try the champion the users has guessed.

        :param message: Command of the user
        :param name: Champion to guess
        """
        emb = None
        text = None
        eph = False

        if self.isPlaying:
            champ = champions.getChamp(name)
            if not champ:
                text = "Champion inconnu."
                eph = True
            else:
                self.loldle.guess(champ)
                last_guess = self.loldle.guesses[0]
                
                desc = (
                    f"{last_guess[0]} `{champ.name}`\n"
                    f"{last_guess[1]} `{champ.gender}`\n"
                    f"{last_guess[2]} `{", ".join(champ.species)}`\n"
                    f"{last_guess[3]} `{", ".join(champ.positions)}`\n"
                    f"{last_guess[4]} `{champ.resource}`\n"
                    f"{last_guess[5]} `{", ".join(champ.range_type)}`\n"
                    f"{last_guess[6]} `{", ".join(champ.regions)}`\n"
                    f"{last_guess[7]} `{champ.release}`\n"
                )

                emb = discord.Embed(
                    title=f"Essaie n°{len(self.loldle.guesses)}: `{name}`", 
                    description=desc, color=cons.emb_color
                )
        else:
            text = "Aucune partie n'est en cours. Lancez une partie avec `/start`."
            eph = True

        await message.response.send_message(embed=emb, content=text, ephemeral=eph)
