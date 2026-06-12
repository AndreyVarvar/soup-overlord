from discord.ext import commands as cmds

from src.bot_core import SoupOverlordCore

def register(soup_overlord: SoupOverlordCore):
    soup_overlord.log("Registering 'on-command-error' event")

    @soup_overlord.bot.event
    async def on_command_error(ctx, error):
        print(error)
