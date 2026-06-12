import discord
from discord.ext import commands as cmds
from src.bot_core import SoupOverlordCore
from src.log import log

def register(soup_overlord: SoupOverlordCore):
    log("Registering 'on-message' event.")

    @soup_overlord.bot.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return  # don't allow bots to trigger the event
