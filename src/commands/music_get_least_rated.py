from discord.ext import commands as cmds
from src.ui.dropdown import RateMusicView
from src.music_database import Track, MusicDatabase
import random

from src.bot_core import SoupOverlordCore
from src.log import log


def register(soup_overlord: SoupOverlordCore):
    name = "music-get-least-rated"
    log(f"Registering '{name}' command.")

    bot: cmds.Bot = soup_overlord.bot
    music_database: MusicDatabase = soup_overlord.music_database

    @bot.hybrid_command(
        name="music-get-least-rated",
        description="Rate a track that is in need of votes"
    )
    async def music_get_least_rated(ctx: cmds.Context):
        if ctx.interaction is None:
            return

        await ctx.interaction.response.defer(ephemeral=True)
        
        user_id = ctx.interaction.user.id

        not_by_user = [entry for entry in music_database.entries if entry.original_sender != user_id]

        if len(not_by_user) == 0:
            await ctx.interaction.followup.send("Sadly, there are no tracks for you to vote on.")
            return

        not_voted_by_user = [entry for entry in not_by_user if user_id not in entry.votes]

        if len(not_voted_by_user) == 0:
            await ctx.interaction.followup.send("WOW, there isn't a single track without your vote!")
            return


        entries_by_votes = {}
        for entry in not_voted_by_user:
            vote_count = len(entry.votes)
            if vote_count not in entries_by_votes:
                entries_by_votes[vote_count] = []

            entries_by_votes[vote_count].append(entry)

        smallest = min(entries_by_votes.keys())

        least_voted: Track = random.choice(entries_by_votes[smallest])

        response = f"Rate `{least_voted.track_name}` by `{least_voted.track_author}` sent by `{least_voted.original_sender}` with just `{smallest}` votes?"
        response += f"\n{least_voted.link}"

        await ctx.interaction.followup.send(response, view=RateMusicView(entry=least_voted, voter=user_id))
