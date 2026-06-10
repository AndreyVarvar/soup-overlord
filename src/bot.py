import discord
from discord.ext import commands as cmds

from src.const import CONFIG

import src.events as events


def init():
    intents = discord.Intents.all()
    command_prefix = "S!"

    bot = cmds.Bot(intents=intents, command_prefix=command_prefix)
    
    events.init(bot)
    
    return bot
        

def run(bot: cmds.Bot):
    token = CONFIG["token"]
    bot.run(token=token)

