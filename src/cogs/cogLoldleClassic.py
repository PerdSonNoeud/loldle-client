import discord
from discord import app_commands

import champions
import constants as cons
from .cogLoldle import CogLoldle
from loldle.loldleClassic import LoldleClassic


def setup(bot):
    return CogLoldleClassic(bot)


class CogLoldleClassic(CogLoldle):
    def __init__(self, client):
        super().__init__(client)
        self.classic = LoldleClassic()
        self.isPlaying = False

    @app_commands.command(name="start-c", description="Commence le mode classique de Loldle.")
    async def startC(self, message: discord.Interaction):
        """
        Function that start a new game.

        :param message: Command of the user
        """
        text = "Une partie est encore en cours !"
        eph = True

        if not self.isPlaying:
            self.isPlaying = True
            self.classic.start()
            text = "Nouvelle partie commencée !"
            eph = False

        await message.response.send_message(content=text, ephemeral=eph)

    @app_commands.command(name="guess-c", description="Deviner un champion pour le mode classique.")
    @app_commands.describe(name="Nom du champion à deviner.")
    @app_commands.autocomplete(name=CogLoldle.autocomplete)
    async def guessC(self, message: discord.Interaction, name: str):
        """
        Function that try the champion the users has guessed.

        :param message: Command of the user
        :param name: Champion to guess
        """
        emb = None
        text = None
        eph = False

        if self.isPlaying:
            champ = champions.get_champ(name)
            if not champ:
                text = "Champion inconnu."
                eph = True
            else:
                found = self.classic.guess(champ)

                if not found:
                    last_guess = self.classic.guesses[0]

                    desc = (
                        f"{last_guess[0]} `{champ.name}`\n"
                        f"{last_guess[1]} `{champ.gender}`\n"
                        f"{last_guess[2]} `{', '.join(champ.species)}`\n"
                        f"{last_guess[3]} `{', '.join(champ.positions)}`\n"
                        f"{last_guess[4]} `{champ.resource}`\n"
                        f"{last_guess[5]} `{', '.join(champ.range_type)}`\n"
                        f"{last_guess[6]} `{', '.join(champ.regions)}`\n"
                        f"{last_guess[7]} `{champ.release}`\n"
                    )

                    emb = discord.Embed(
                        title=f"Essai n°{len(self.classic.guesses)}: `{name}`",
                        description=desc,
                        color=cons.emb_color,
                    )
                else:
                    emb = discord.Embed(
                        title=f"Trouvé, c'était `{self.classic.champ.name}` !",
                        description=self.classic,
                        color=cons.emb_color,
                    )
                    print(self.classic.champ.get_url())
                    emb.set_image(url=self.classic.champ.get_url())
                    self.isPlaying = False

        else:
            text = "Aucune partie n'est en cours. Lancez une partie avec `/start-c`."
            eph = True

        await message.response.send_message(embed=emb, content=text, ephemeral=eph)
