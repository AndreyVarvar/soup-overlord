from discord.ext import commands as cmds

from src.bot_core import SoupOverlordCore
from src.log import log


def register(soup_overlord: SoupOverlordCore):
    name = "help"

    log(f"Registering '{name}' command")
    bot = soup_overlord.bot

    @bot.hybrid_command(
        name=name,
        description="Get help regarding the bot"
    )
    async def help(ctx: cmds.Context):
        if ctx.interaction is None:
            return

        await ctx.interaction.response.send_message("Just ask @andreyvarvar :P")
