import discord
from discord.ext import commands as cmds
from .add_music import add_music_to_database

async def process_message_for_music(bot: cmds.Bot, message: discord.Message, spotipy_client):
    code, response = await add_music_to_database(bot, message, spotipy_client)

    if code == 1:
        pass
    elif code == -1:
        await message.reply("This track was already shared before!")
        await message.add_reaction('\u267B')  # react with a recycle icon
    elif code == 0:
        await message.add_reaction('\u2B50')  # make a visual cue everything is okay

    elif code == 2:
        await message.reply(response)


async def on_message_gif_channel(message: discord.Message):
    pass
