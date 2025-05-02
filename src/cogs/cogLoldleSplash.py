from io import BytesIO

import discord
from discord import app_commands

import champions
import constants as cons
from loldle.loldleSplash import LoldleSplash

from .cogLoldle import CogLoldle


def setup(bot):
    return CogLoldleSplash(bot)


class CogLoldleSplash(CogLoldle):
    def __init__(self, client):
        super().__init__(client)
        self.splash = LoldleSplash()
        self.isPlaying = False

    @app_commands.command(name="start-s", description="Commence le mode splash de Loldle.")
    async def startS(self, message: discord.Interaction):
        """
        Function that start a new game.

        :param message: Command of the user
        """
        text = "Une partie est encore en cours !"
        file = None
        eph = True

        if not self.isPlaying:
            self.isPlaying = True
            self.splash.start()
            eph = False
            emb = discord.Embed(
                title="Nouvelle partie commencée !",
                description="Quel champion a le splash art complet ?",
                color=cons.emb_color,
            )
            splash = self.splash.get_splash(True)
            if type(splash) is str:
                emb.set_image(url=splash)
                await message.response.send_message(embed=emb, ephemeral=eph)
            else:
                buffer = BytesIO()
                splash.save(buffer, format="PNG")
                buffer.seek(0)
                file = discord.File(buffer, filename="splash.png")
                emb.set_image(url="attachment://splash.png")
                await message.response.send_message(embed=emb, file=file, ephemeral=eph)
        else:
            await message.response.send_message(content=text, ephemeral=eph)

    @app_commands.command(name="guess-s", description="Devine le champion de Loldle.")
    @app_commands.describe(name="Nom du champion à deviner.")
    @app_commands.autocomplete(name=CogLoldle.autocomplete)
    async def guessS(self, message: discord.Interaction, name: str):
        """
        Function that guesses if a champion is right.

        :param name: Name of the champion
        """
        emb = None
        text = None
        eph = False
        view = None

        if self.isPlaying:
            champ = champions.get_champ(name)
            if champ is None:
                text = "Champion introuvable !"
                eph = True
            else:
                found = self.splash.guess(champ)
                if found:
                    self.isPlaying = False
                    emb = discord.Embed(
                        title="Partie terminée !",
                        description=f"Le champion était {self.splash.champ.name} !",
                        color=cons.emb_color,
                    )
                    view = SplashView(self.splash)
                else:
                    last_guess = self.splash.guesses[0]

                    emb = discord.Embed(
                        title=f"Essai n°{len(self.splash.guesses)}: `{name}`",
                        description=f"{last_guess[0]} {last_guess[1]}",
                        color=cons.emb_color,
                    )
                splash = self.splash.get_splash(not found)
                if type(splash) is str:
                    emb.set_image(url=splash)
                else:
                    buffer = BytesIO()
                    splash.save(buffer, format="PNG")
                    buffer.seek(0)
                    file = discord.File(buffer, filename="splash.png")
                    emb.set_image(url="attachment://splash.png")
                    await message.response.send_message(embed=emb, file=file, ephemeral=eph)
                    return

        else:
            text = "Aucune partie n'est en cours. Lancez une partie avec `/start-s`."
            eph = True
        if view is None:
            await message.response.send_message(embed=emb, content=text, ephemeral=eph)
        else:
            await message.response.send_message(embed=emb, view=view, ephemeral=eph)


class SplashSelect(discord.ui.Select):
    def __init__(self, splash):
        options = [discord.SelectOption(label=skin["name"]) for skin in splash.champ.skins]
        super().__init__(placeholder="Quel est le nom du Splash ?", options=options)
        self.splash = splash

    async def callback(self, interaction: discord.Interaction):
        splash = self.values[0]
        result = self.splash.name
        if result == splash:
            title = "Bien vu !"
        else:
            title = "Dommage !"
        text = f"C'était le skin {result} !"
        embed = discord.Embed(title=title, description=text, color=cons.emb_color)
        embed.set_image(url=self.splash.get_splash())
        await interaction.response.send_message(embed=embed, ephemeral=False)


class SplashView(discord.ui.View):
    def __init__(self, splash):
        super().__init__()
        self.add_item(SplashSelect(splash))
