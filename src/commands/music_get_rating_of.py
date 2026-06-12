from discord.ext import commands as cmds
import discord

from src.ui.embed import make_music_rating_embed

from src.music_database import MusicDatabase

from src.bot_core import SoupOverlordCore


def register(soup_overlord: SoupOverlordCore):
    name = "music-get-rating-of"
    soup_overlord.log(f"Registering '{name}' command")
    bot: cmds.Bot = soup_overlord.bot
    music_database: MusicDatabase = soup_overlord.music_database

    @bot.hybrid_command(
        name=name,
        description="Get a rating of a specific track"
    )
    async def music_get_rating_of(
        ctx: cmds.Context, 
        track_name: str | None = None, 
        track_author: str | None = None,
        sent_by: discord.Member | None = None     
    ):
        if ctx.interaction is None:
            return

        await ctx.interaction.response.defer(ephemeral=True)
    
        if track_name is None and track_author is None and sent_by is None:
            await ctx.interaction.followup.send("You need to specify at least one criteria.")
            return

        entries = music_database.entries.copy()
    
        if track_name is not None:
            entries = [entry for entry in entries if track_name.upper() in entry.track_name.upper()]

        if track_author is not None:
            entries = [entry for entry in entries if track_author.upper() in entry.track_author.upper()]

        if sent_by is not None:
            entries = [entry for entry in entries if sent_by.id == entry.original_sender]

        if len(entries) == 0:
            await ctx.interaction.followup.send("No track with the given query was found.")
            return

        if len(entries) == 1:
            entry = entries[0]
            
            embed = make_music_rating_embed(entry, soup_overlord)
    
            await ctx.interaction.followup.send(embed=embed)
            return

        if len(entries) <= 6:
            responses = []
            for entry in entries:
                responses.append(f"- Track `{entry.track_name}` by `{entry.track_author}` sent by `{soup_overlord.get_cached_name(entry.original_sender)}`")
            
            response = f"There are a total of {len(entries)} entries that match your result:\n" + '\n'.join(responses) + "\nPlease use this command again, but with a more specific query."
            await ctx.interaction.followup.send(response)
            return

        
        await ctx.interaction.followup.send(f"Search query is too vague, there are multiple tracks with similar criterias ({len(entries)} entries found)")

