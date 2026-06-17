from discord.ext import commands as cmds
import discord

from src.bot_core import SoupOverlordCore


def register(soup_overlord: SoupOverlordCore):
    name = "echo"
    soup_overlord.log(f"Registering '{name}' command.")
    bot = soup_overlord

    @bot.hybrid_command(
        name=name,
        description="Echoes whatever you say into another channel"
    )
    @cmds.is_owner()
    async def echo(ctx: cmds.Context, message: str, channel: discord.channel.TextChannel | None = None):
        if ctx.interaction is None:
            return

        await ctx.interaction.response.send_message("Used echo", ephemeral=True)

        if channel is None:
            channel = ctx.interaction.channel

        await soup_overlord.discord_log(
            f"Echoed message by `{ctx.interaction.user.display_name}` in the channel `#{channel.name}`"
        )

        await channel.send(message)


