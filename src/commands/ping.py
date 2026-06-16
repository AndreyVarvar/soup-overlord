from discord.ext import commands as cmds 

from src.bot_core import SoupOverlordCore


def register(soup_overlord: SoupOverlordCore):
    name = "ping"
    soup_overlord.log(f"Registering '{name}' command")

    bot: cmds.Bot = soup_overlord

    @bot.hybrid_command(
        name=name,
        description="ping pong"
    )
    async def ping(ctx: cmds.Context):
        if ctx.interaction is None:
            return
        await ctx.interaction.response.defer()

        await ctx.interaction.followup.send("Pong!")
