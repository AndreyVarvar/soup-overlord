from discord.ext import commands as cmds
from src.music_database import MusicDatabase
from src.bot_core import SoupOverlordCore
from datetime import datetime

import pygame as pg


def register(soup_overlord: SoupOverlordCore):
    name = "music-wrapped"
    soup_overlord.log(f"Registering '{name}' command.")

    bot: cmds.Bot = soup_overlord
    music_database: MusicDatabase = soup_overlord.music_database

    @bot.hybrid_command(
        name=name,
        description="Shows how many entries you haven't rated yet"
    )
    async def music_wrapped(ctx: cmds.Context, year: int):
        if ctx.interaction is None:
            return
        
        await ctx.interaction.response.defer(ephemeral=True)

        if year > datetime.now().year+1 or year < 2024:
            await ctx.interaction.followup.send(f"Invalid year: `{year}`")

        pie_chart = pg.Surface((200, 200))
        pie_chart.fill("white")

        
 
        # We generate a wrapped by the following criterias:
        # 1) how many songs shared each month
        # 2) most popular artist overall
        # 3) Leaderboard of who sent the most tracks
        # 4) Top-music sender by month
        # 5) How many tracks shared overall
        
        # Generate a pie chart for the 1) and 5) 


