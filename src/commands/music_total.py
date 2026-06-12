from discord.ext import commands as cmds

from src.music_database import MusicDatabase

from src.bot_core import SoupOverlordCore


def register(soup_overlord: SoupOverlordCore):
    name = "music-total"
    soup_overlord.log(f"Registering '{name}' command.")

    bot: cmds.Bot = soup_overlord.bot
    music_database: MusicDatabase = soup_overlord.music_database

    @bot.hybrid_command(
        name=name,
        description="Shows how many tracks were shared"
    )
    async def music_total(ctx: cmds.Context):
        if ctx.interaction is None:
            return

        await ctx.interaction.response.defer(ephemeral=True)

        amount = len(music_database.entries)

        await ctx.interaction.followup.send(f"There are currently a total of {amount} entires in the database.")

