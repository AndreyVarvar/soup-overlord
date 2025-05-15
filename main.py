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

# init the spotipy
SPOTIFY_CLIENT = spotify_init.init_sp(config['spotify']['clientId'], config['spotify']['clientSecret'])


# ------------------------------------------------------------ EVENTS ------------------------------------------------------------
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

# ------------------------------------------------------------ COMMANDS ------------------------------------------------------------
@command_tree.context_menu(
    name='Add music',
    guild=discord.Object(id=const.SERVER_ID)
)
async def add_music(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer()
    code, response = await music_add(message, SPOTIFY_CLIENT)

    if code == 1:
        await interaction.followup.send("This message does not contain a spotify link.")
    elif code == -1:
        await interaction.followup.send("This track was already shared before!")
    elif code == 0:
        await interaction.followup.send(response)
        await message.add_reaction("<:confirmed:1291384088950997032>")  # make a visual cue everything is okay

    elif code == 2:
        await interaction.followup.send(response)


# ------------------------------------------------------------ DISCORD RUN ------------------------------------------------------------
client.run(config['discord']['token'])
