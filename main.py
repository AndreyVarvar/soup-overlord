import discord
import json

from utils import spotify_init
from utils.add_music import add_music as music_add
from utils import const

from src import events
from src import commands


config: dict
# get the token from 'config.json'
with open('config.json', 'r') as file:
    config = json.load(file)

# setup
intents = discord.Intents.all()
intents.message_content = True

SoupOverlord = discord.Client(intents=intents)
command_tree = discord.app_commands.CommandTree(SoupOverlord)

# init the spotipy
SPOTIFY_CLIENT = spotify_init.init_sp(config['spotify']['clientId'], config['spotify']['clientSecret'])


events.init_events(SoupOverlord, command_tree, SPOTIFY_CLIENT)
commands.init_commands(command_tree, SPOTIFY_CLIENT)


SoupOverlord.run(config['discord']['token'])
