from discord.ext import commands as cmds
from src.music_database import MusicDatabase
from ui.dropdown import RateMusicView

import random


def register(bot: cmds.Bot, music_database: MusicDatabase):
    @bot.hybrid_command(
        name="music-rate-random",
        description="Get a random track to rate"
    )
    async def music_random_unrated(ctx: cmds.Context):
        if ctx.interaction is None:  # to appease type-hinting
            return

        await ctx.interaction.response.defer(ephemeral=True)

        user_id = ctx.interaction.user.id

        not_by_user = {entry for entry in music_database.entries if entry.original_sender != user_id}

        if len(not_by_user) == 0:
            await ctx.interaction.followup.send("Sadly, there are no tracks for you to vote on.")
            return

        # clean up the data a little
        not_voted_by_user = []
        for entry in not_by_user:
            if user_id not in entry.voters:
                not_voted_by_user.append(entry)
        
        if len(not_voted_by_user) == 0:
            await ctx.interaction.followup.send("WOW, there isn\'t a single track that doesn\'t have your vote!")
            return
        

        random_unvoted = random.choice(not_voted_by_user)

        response = f'What would you rate `{random_unvoted.track_name}` by `{random_unvoted.track_author}` sent by `{random_unvoted.original_sender}`?'
        response += f'\n{random_unvoted.link}'
        
        await ctx.interaction.followup.send(response, view=RateMusicView(entry=random_unvoted, voter=user_id))

