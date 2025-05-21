import discord
from .add_music import add_music_to_database

async def process_message_for_music(message: discord.Message, spotipy_client):
    code, response = await add_music_to_database(message, spotipy_client)

    if code == 1:
        pass
    elif code == -1:
        message.reply("This track was already shared before!")
    elif code == 0:
        await message.add_reaction("<:confirmed:1291384088950997032>")  # make a visual cue everything is okay

    elif code == 2:
        await message.reply(response)


async def on_message_gif_channel(message: discord.Message):
    pass
