from discord.ext import commands as cmds

from src.music_database import MusicDatabase

from src.bot_core import SoupOverlordCore

import random


def register(soup_overlord: SoupOverlordCore):
    name = "music-list-top-rated"
    soup_overlord.log(f"Registering '{name}' command.")

    bot: cmds.Bot = soup_overlord
    music_database: MusicDatabase = soup_overlord.music_database

    @bot.hybrid_command(
        name=name,
        description="Shows top-rated songs of the Soup Nation discord"
    )
    async def music_list_top_rated(ctx: cmds.Context):
        if ctx.interaction is None:
            return

        count = 10

        await ctx.interaction.response.defer(ephemeral=True)
       
        top_rated = music_database.entries.copy()
        random.shuffle(top_rated)
        top_rated.sort(key=lambda entry: -sum(entry.votes.values())/len(entry.votes.values()) if len(entry.votes) > 0 else 0)

        responses = []
        for i, entry in enumerate(top_rated[:count]):
            responses.append(f"{i+1}) Track `{entry.track_name}` by `{entry.track_author}` with average rating of `{sum(entry.votes.values())/len(entry.votes.values()):.2f}`")
        
        response = '\n'.join(responses)
        await ctx.interaction.followup.send(response)
        return
