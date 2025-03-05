import discord
from discord import app_commands

import champions
import constants as cons
from cogLoldle import CogLoldle
from loldleAbility import LoldleAbility


class CogLoldleAbility(CogLoldle):
    def __init__(self, client):
        super().__init__(client)
        self.ability = LoldleAbility()
        self.isPlaying = False

    @app_commands.command(name="start-a", description="Commence le mode Compétence de Loldle.")
    async def startA(self, message: discord.Interaction):
        """
        Function that start a new game.

        :param message: Command of the user
        """
        text = "Une partie est encore en cours !"
        emb = None
        eph = True

        if not self.isPlaying:
            self.isPlaying = True
            self.ability.start()
            text = None
            emb = discord.Embed(
                title="Nouvelle partie commencée !",
                description="Quel champion a cette compétence ?",
                color=cons.emb_color,
            )
            url = self.ability.get_icon()
            emb.set_thumbnail(url=url)
            text = None
            eph = False

        await message.response.send_message(content=text, embed=emb, ephemeral=eph)

    @app_commands.command(name="guess-a", description="Deviner pour le mode Compétence.")
    @app_commands.describe(name="Nom du champion à deviner.")
    @app_commands.autocomplete(name=CogLoldle.autocomplete)
    async def guessA(self, message: discord.Interaction, name: str):
        """
        Function that guesses if a champion is right.

        :param name: Name of the champion
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
                found = self.ability.guess(champ)

                if not found:
                    last_guess = self.ability.guesses[0]

                    emb = discord.Embed(
                        title=f"Essai n°{len(self.ability.guesses)}: `{name}`",
                        description=f"{last_guess[0]} {last_guess[1]}",
                        color=cons.emb_color,
                    )
                else:
                    emb = discord.Embed(
                        title=f"Trouvé, c'était `{name}` !",
                        description=self.ability,
                        color=cons.emb_color,
                    )
                    self.isPlaying = False
                url = self.ability.get_icon()
                emb.set_thumbnail(url=url)

        else:
            text = "Aucune partie n'est en cours. Lancez une partie avec `/start-a`."
            eph = True

        await message.response.send_message(embed=emb, content=text, ephemeral=eph)
