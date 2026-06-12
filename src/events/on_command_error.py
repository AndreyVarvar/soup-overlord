from discord.ext import commands as cmds

from src.bot_core import SoupOverlordCore
from src.log import log

def register(soup_overlord: SoupOverlordCore):
    log("Registering 'on-command-error' event")

    @soup_overlord.bot.event
    async def on_command_error(ctx, error):
        print(error)
