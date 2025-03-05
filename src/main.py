import discord
from discord.ext import commands

from cogLoldleOther import CogLoldleOther
from cogLoldleClassic import CogLoldleClassic
from cogLoldleAbility import CogLoldleAbility

with open("./assets/token.txt", "r") as file:
    token = file.read()


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="/", intents=intents, help_command=None)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("-----")

    try:
        # Add the cogs
        await client.add_cog(CogLoldleOther(client))
        await client.add_cog(CogLoldleClassic(client))
        await client.add_cog(CogLoldleAbility(client))
        # Sync the commands
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


client.run(token)
