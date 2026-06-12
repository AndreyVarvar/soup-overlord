from discord.ext import commands as cmds

from . import on_ready, on_message, on_command_error
from src.bot_core import SoupOverlordCore

from src.log import log

def init(bot: SoupOverlordCore):
    log("Registering events.")
    on_ready.register(bot)
    on_message.register(bot)
    on_command_error.register(bot)

