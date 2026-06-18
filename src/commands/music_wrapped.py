from discord.ext import commands as cmds
from src.music_database import MusicDatabase
from src.bot_core import SoupOverlordCore
from datetime import datetime

import json


from src.ui.embeds.wrapped_embed import \
    WrappedShareCountEmbed, \
    WrappedMostPopularArtistEmbed, \
    WrappedTopSharerEmbed, \
    WrappedTopCriticEmbed, \
    WrappedMostLovedTrackSendersEmbed, \
    WrappedMostLovedTracksEmbed


def register(soup_overlord: SoupOverlordCore):
    name = "music-wrapped"
    soup_overlord.log(f"Registering '{name}' command.")

    bot: cmds.Bot = soup_overlord
    music_database: MusicDatabase = soup_overlord.music_database

    @bot.hybrid_command(
        name=name,
        description="Show a wrapped for the specified year"
    )
    @cmds.has_permissions(administrator=True)
    async def music_wrapped(ctx: cmds.Context, year: int):
        if ctx.interaction is None:
            return
        

        if year > datetime.now().year or year < 2024:
            await ctx.interaction.response.send_message(f"Invalid year: `{year}`", ephemeral=True)
            return

        if year == datetime.now().year:
            await ctx.interaction.response.send_message(f"The year `{year}` did not end yet", ephemeral=True)
            return


        with open("wrapped.json", "r") as file:
            wrapped = json.load(file)
        
        if year in wrapped["years_covered"]:
            await ctx.interaction.response.send_message(f"The year `{year}` already has a wrapped generated", ephemeral=True)
            return

        await ctx.interaction.response.defer()

        wrapped["years_covered"].append(year)
        with open("wrapped.json", "w") as file:
            file.write(str(wrapped))

        tracks_this_year = music_database.filter(lambda entry: entry.created_at.year == year)
    
        await ctx.interaction.followup.send(
            embeds=[
                await WrappedShareCountEmbed.build(soup_overlord, tracks_this_year, year),
                await WrappedMostPopularArtistEmbed.build(soup_overlord, tracks_this_year, year),
                await WrappedTopSharerEmbed.build(soup_overlord, tracks_this_year, year),
                await WrappedTopCriticEmbed.build(soup_overlord, tracks_this_year, year),
                await WrappedMostLovedTrackSendersEmbed.build(soup_overlord, tracks_this_year, year),
                await WrappedMostLovedTracksEmbed.build(soup_overlord, tracks_this_year, year),
            ]
        )

