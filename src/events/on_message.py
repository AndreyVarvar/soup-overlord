import discord
from discord.ext import commands as cmds

def register(bot: cmds.Bot):
    @bot.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return  # don't allow bots to trigger the event
