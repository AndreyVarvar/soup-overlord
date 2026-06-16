from discord.ext import commands as cmds
import discord

from src.music_database import MusicDatabase

from src.bot_core import SoupOverlordCore


def register(soup_overlord: SoupOverlordCore):
    name = "music-filter"
    soup_overlord.log(f"Registering '{name}' command")
    bot: cmds.Bot = soup_overlord
    music_database: MusicDatabase = soup_overlord.music_database

    @bot.hybrid_command(
        name=name,
        description="Get tracks that match your query."
    )
    async def music_filter(
        ctx: cmds.Context, 
        track_name_contains: str | None = None, 
        track_author_contains: str | None = None,
        sent_by: discord.Member | None = None,
        track_name_does_not_contain: str | None = None,
        track_author_does_not_contain: str | None = None,
        not_sent_by: discord.Member | None = None
    ):
        if ctx.interaction is None:
            return

        await ctx.interaction.response.defer(ephemeral=True)
    
        if track_name_contains is None and \
            track_author_contains is None and \
            sent_by is None and \
            track_name_does_not_contain is None and \
            track_author_does_not_contain is None and \
            not_sent_by is None:
            await ctx.interaction.followup.send("You need to specify at least one criteria.")
            return

        entries = music_database.filter(
            lambda entry: \
                (track_name_contains is None or track_name_contains.upper() in entry.track_name.upper()) and \
                (track_author_contains is None or track_author_contains.upper() in entry.track_author.upper()) and \
                (sent_by is None or sent_by.id == entry.original_sender) and \
                (track_name_does_not_contain is None or track_name_does_not_contain.upper() not in entry.track_name.upper()) and \
                (track_author_does_not_contain is None or track_author_does_not_contain.upper() not in entry.track_author.upper()) and \
                (not_sent_by is None or not_sent_by.id != entry.original_sender)
        ) 

        if len(entries) == 0:
            await ctx.interaction.followup.send("No track with the given query was found.")
            return

        if len(entries) <= 20:
            responses = []
            for entry in entries:
                responses.append(f"- Track `{entry.track_name}` by `{entry.track_author}` sent by `{soup_overlord.get_cached_name(entry.original_sender)}`")
            
            response = f"There are a total of {len(entries)} entries that match your query:\n" + '\n'.join(responses)
            await ctx.interaction.followup.send(response)
            return

        
        await ctx.interaction.followup.send(f"Search query is too vague, there are too many tracks that satisfy your query ({len(entries)} entries found)")

