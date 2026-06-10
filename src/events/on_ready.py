from discord.ext import commands as cmds
import discord

from src.const import CONFIG
from src.log import log

def register(bot: cmds.Bot):
    @bot.event
    async def on_ready():
        bot.tree.clear_commands(guild=discord.Object(id=int(CONFIG['serverID'])))
        await bot.tree.sync()
        await bot.tree.sync(guild=discord.Object(id=int(CONFIG['serverID'])))
        
        log("\n", timestamp=False)
        log("Bot startup")
