import discord
from src.bot_core import SoupOverlordCore

def register(soup_overlord: SoupOverlordCore):
    soup_overlord.log("Registering 'on-command-error' event")

    @soup_overlord.bot.event
    async def on_command_error(ctx, error):
        soup_overlord.log(str(error))
        await soup_overlord.discord_log("An error has occured. Check the logs for more information.")
        
