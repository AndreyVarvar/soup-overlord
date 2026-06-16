from discord.ext import commands as cmds

from src.music_database import MusicDatabase

from src.bot_core import SoupOverlordCore

import random


def register(soup_overlord: SoupOverlordCore):
    name = "music-list-my-top-rated"
    soup_overlord.log(f"Registering '{name}' command.")

    bot: cmds.Bot = soup_overlord
    music_database: MusicDatabase = soup_overlord.music_database

    @bot.hybrid_command(
        name=name,
        description="Shows top-rated songs of the Soup Nation discord that were sent by you"
    )
    async def music_list_my_top_rated(ctx: cmds.Context):
        if ctx.interaction is None:
            return

        count = 10

        await ctx.interaction.response.defer(ephemeral=True)

        user_id = ctx.interaction.user.id
       
        top_rated = music_database.filter(lambda entry: entry.original_sender == user_id)
        random.shuffle(top_rated)
        top_rated.sort(key=lambda entry: -sum(entry.votes.values())/len(entry.votes.values()) if len(entry.votes) > 0 else 0)

        responses = []
        for i, entry in enumerate(top_rated[:count]):
            responses.append(f"{i+1}) Track `{entry.track_name}` by `{entry.track_author}` with average rating of `{sum(entry.votes.values())/len(entry.votes.values()):.2f}`")
        
        response = '\n'.join(responses)
        await ctx.interaction.followup.send(response)
        return
