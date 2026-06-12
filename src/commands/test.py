from discord.ext import commands as cmds

from src.bot_core import SoupOverlordCore
from src.log import log


def register(soup_overlord: SoupOverlordCore):
    name = "test"
    log(f"Registering '{name}' command")

    bot: cmds.Bot = soup_overlord.bot

    @bot.hybrid_command(
        name=name,
        description="test"
    )
    @cmds.is_owner()
    async def test(ctx: cmds.Context):
        if ctx.interaction is None:
            return

        await ctx.interaction.response.send_message('test successful', ephemeral=True)
