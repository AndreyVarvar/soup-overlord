import discord
from discord.ext import commands as cmds

from src.const import CONFIG

# setup
intents = discord.Intents.all()

SoupOverlord = cmds.Bot(intents=intents, command_prefix="$")
SoupOverlord.run(CONFIG['discord']['token'])
