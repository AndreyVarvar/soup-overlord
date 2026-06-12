from discord.ext import commands as cmds
import discord
from src.ui.dropdown import RateMusicView
from src.music_database import MusicDatabase

from src.bot_core import SoupOverlordCore
from src.log import log


def register(soup_overlord: SoupOverlordCore):
    name = "music-rate-specific"
    log(f"Registering '{name}' command.")
    bot: cmds.Bot = soup_overlord.bot
    music_database: MusicDatabase = soup_overlord.music_database

    @bot.hybrid_command(
        name=name,
        description="Rate a track you know the name of"
    )
    async def music_rate_specific(
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

        user_id = ctx.interaction.user.id

        entries = [entry for entry in music_database.entries if entry.original_sender != user_id]

        if track_name is not None:
            entries = [entry for entry in entries if track_name.upper() in entry.track_name.upper()]

        if track_author is not None:
            entries = [entry for entry in entries if track_author.upper() in entry.track_author.upper()]

        if sent_by is not None:
            entries = [entry for entry in entries if sent_by.id == entry.original_sender]
        
        if len(entries) == 0:
            await ctx.interaction.followup.send("No tracks with such criterias were found")
            return
        
        if len(entries) == 1:
            entry = entries[0]

            old_vote = entry.votes[user_id] if user_id in entry.votes else None

            response = f'What would you rate `{entry.track_name}` by `{entry.track_author}` sent by `{entry.original_sender}`?'  # TODO: turn original_sender into actual name
            if old_vote is not None:
                response += f" Your previous vote was `{old_vote}`."
            response += f"\n{entry.link}"

            await ctx.interaction.followup.send(response, view=RateMusicView(entry=entry, voter=user_id))
            return

       
        to_show = 20
        if len(entries) <= to_show:  # will show `to_show` many tracks that matched the query
            responses = []
            for entry in entries:
                responses.append(f"- Track `{entry.track_name}` by `{entry.track_author}` sent by `{entry.original_sender}`")  # TODO: fix the origial sender thing
            
            response = f"There are a total of {len(entries)} entries that match your result:\n" + '\n'.join(responses) + "\nPlease use this command again, but with more specific details."
            await ctx.interaction.followup.send(response)
            return
        
        await ctx.interaction.followup.send(f"Search query is too vague, there are multiple tracks with similar names ({len(entries)} entries found)")
