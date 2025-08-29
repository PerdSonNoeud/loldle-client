import discord
from discord.ext import commands

import cogs


try:
    with open("./assets/TOKEN.txt", "r") as file:
        token = file.read()
except Exception as e:
    print("File not found, no token were given.")
    exit(2)


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="/", intents=intents, help_command=None)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("-----")

    try:
        # Add the cogs
        await cogs.setup(client)
        # Sync the commands
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


client.run(token)
