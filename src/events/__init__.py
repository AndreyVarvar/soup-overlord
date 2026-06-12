from discord.ext import commands as cmds

from . import on_ready, on_message, on_command_error
from src.bot_core import SoupOverlordCore


def init(soup_overlord: SoupOverlordCore):
    soup_overlord.log("Registering events.")
    on_ready.register(soup_overlord)
    on_message.register(soup_overlord)
    on_command_error.register(soup_overlord)

