import discord
import json

from utils import spotify_init
from utils.log import log
from utils.special_channels import process_message_for_music, on_message_gif_channel
from utils.add_music import add_music as music_add
from utils import const


config: dict
# get the token from 'config.json'
with open('config.json', 'r') as file:
    config = json.load(file)

# setup
intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)
command_tree = discord.app_commands.CommandTree(client)


SPECIAL_CHANNELS = {
    const.MUSIC_CHANNEL: process_message_for_music,  # music channel
    const.GIF_WARS_CHANNEL: on_message_gif_channel,  # gif-wars channel
    const.GOOFING_AROUND: lambda x, y: 0  # ignore
}

# init the spotipy
SPOTIFY_CLIENT = spotify_init.init_sp(config['spotify']['clientId'], config['spotify']['clientSecret'])

@client.event
async def on_ready():
    await command_tree.sync(guild=discord.Object(id=const.SERVER_ID))
    log("\n")
    log("Bot startup")

@client.event
async def on_connect():
    log("Bot online")

@client.event
async def on_disconnect():
    log("Bot offline")

@client.event
async def on_message(message: discord.Message):
    channel_id = message.channel.id

    if channel_id == const.MUSIC_CHANNEL:
        await process_message_for_music(message, SPOTIFY_CLIENT)

@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    # print(f"{user.name} reacted with {reaction.emoji}")
    pass


@command_tree.command(
    name='add-music',
    description='add music from another message to the database',
    guild=discord.Object(id=const.SERVER_ID)
)
async def add_music(interaction: discord.Interaction, message_id: str):
    await interaction.response.defer(ephemeral=True)
    try:
        message = await interaction.channel.fetch_message(int(message_id))
        print(message)
        await music_add(message, SPOTIFY_CLIENT)
        await interaction.followup.send("Successful command invocation.", ephemeral=True)
    except discord.errors.NotFound:
        await interaction.followup.send("Invalid 'message_id'.", ephemeral=True)


client.run(config['discord']['token'])
