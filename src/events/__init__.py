from discord.ext import commands as cmds

from . import on_ready, on_message, on_command_error


def init(bot: cmds.Bot):
    on_ready.register(bot)
    on_message.register(bot)
    on_command_error.register(bot)

