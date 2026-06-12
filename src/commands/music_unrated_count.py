from discord.ext import commands as cmds

from src.music_database import MusicDatabase

from src.bot_core import SoupOverlordCore


def register(soup_overlord: SoupOverlordCore):
    name = "music-unrated-count"
    soup_overlord.log(f"Registering '{name}' command.")

    bot: cmds.Bot = soup_overlord.bot
    music_database: MusicDatabase = soup_overlord.music_database

    @bot.hybrid_command(
        name=name,
        description="Shows how many entries you haven't rated yet"
    )
    async def music_unrated_count(ctx: cmds.Context):
        if ctx.interaction is None:
            return

        await ctx.interaction.response.defer(ephemeral=True)
        entries = music_database.entries.copy()
        total_unvoted = 0
        
        user_id = ctx.interaction.user.id

        for entry in entries:
            if user_id not in entry.votes and user_id != entry.original_sender:
                total_unvoted += 1
        
        if total_unvoted == 0:
            await ctx.interaction.followup.send("WOW, there isn't a single track you haven't voted on!")
            return
        
        if total_unvoted == 1:
            await ctx.interaction.followup.send(f"You have only 1 unvoted track.")

        await ctx.interaction.followup.send(f"You haven't rated a total of `{total_unvoted}` tracks.")
