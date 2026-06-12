from discord.ext import commands as cmds
import discord

from src.bot_core import SoupOverlordCore
from src.log import log


def register(soup_overlord: SoupOverlordCore):
    name = "echo"
    log(f"Registering '{name}' command.")
    bot = soup_overlord.bot

    @bot.hybrid_command(
        name=name,
        description="Echoes whatever you say into another channel"
    )
    @cmds.is_owner()
    async def echo(ctx: cmds.Context, message: str, channel: discord.channel.TextChannel | None = None):
        if ctx.interaction is None:
            return

        await ctx.interaction.response.send_message("Used echo", ephemeral=True)

        if channel is not None:
            await channel.send(message)
        else:
            await ctx.send(message)
