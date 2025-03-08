from io import BytesIO

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
        self.filter = True

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
            icon = self.ability.get_icon(self.filter)
            if type(icon) is str:
                emb.set_thumbnail(url=icon)
            else:
                buffer = BytesIO()
                icon.save(buffer, format="PNG")
                buffer.seek(0)
                file = discord.File(buffer, filename="ability.png")
                emb.set_thumbnail(url="attachment://ability.png")
                await message.response.send_message(embed=emb, file=file)
                return
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
        view = None

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
                    icon = self.ability.get_icon(self.filter)
                else:
                    emb = discord.Embed(
                        title=f"Trouvé, c'était `{name}` !",
                        description=self.ability.name,
                        color=cons.emb_color,
                    )
                    emb.add_field(name="", value=f"{self.ability}")
                    view = AbilityView(self.ability)
                    self.isPlaying = False
                    icon = self.ability.get_icon(False)

                if type(icon) is str:
                    emb.set_thumbnail(url=icon)
                else:
                    buffer = BytesIO()
                    icon.save(buffer, format="PNG")
                    buffer.seek(0)
                    file = discord.File(buffer, filename="ability.png")
                    emb.set_thumbnail(url="attachment://ability.png")
                    await message.response.send_message(embed=emb, file=file, ephemeral=eph)
                    return

        else:
            text = "Aucune partie n'est en cours. Lancez une partie avec `/start-a`."
            eph = True
        if view is None:
            await message.response.send_message(embed=emb, content=text, ephemeral=eph)
        else:
            await message.response.send_message(embed=emb, view=view, ephemeral=eph)

    @app_commands.command(name="toggle_filter", description="Active/Désactive les filtres pour le mode compétence.")
    async def toggle_filter(self, message: discord.Interaction):
        self.filter = not self.filter
        await message.response.send_message(content=f"Le mode filtre a été mis à {self.filter}.")


def switch_name(ability: str):
    if "passive" in ability:
        return "p"
    if "Pre" in ability:
        return "q"
    if "Deu" in ability:
        return "w"
    if "Tro" in ability:
        return "e"
    return "r"


class AbilitySelect(discord.ui.Select):
    def __init__(self, ability):
        options = [
            discord.SelectOption(label="Compétence passive", emoji="🇵"),
            discord.SelectOption(label="Première compétence", emoji="🇶"),
            discord.SelectOption(label="Deuxième compétence", emoji="🇼"),
            discord.SelectOption(label="Troisième compétence", emoji="🇪"),
            discord.SelectOption(label="Compétence ultime", emoji="🇷"),
        ]
        super().__init__(placeholder="Quel est ce sort ?", options=options)
        self.ability = ability

    async def callback(self, interaction: discord.Interaction):
        ability = switch_name(self.values[0])
        result = self.ability.ability
        if result == ability:
            title = "Bien vu !"
        else:
            title = "Dommage !"
        text = f"C'était le {result if result != 'p' else 'passif'} "
        text += f"de {self.ability.champ.name} !"
        embed = discord.Embed(title=title, description=text, color=cons.emb_color)
        embed.add_field(name=f"{self.ability.name}", value="")
        embed.set_thumbnail(url=self.ability.get_icon())
        await interaction.response.send_message(embed=embed, ephemeral=False)


class AbilityView(discord.ui.View):
    def __init__(self, ability):
        super().__init__()
        self.add_item(AbilitySelect(ability))
