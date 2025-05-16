import discord

from utils import spotify_init
from utils import const

from src import events
from src import commands


# setup
intents = discord.Intents.all()
intents.message_content = True

SoupOverlord = discord.Client(intents=intents)
command_tree = discord.app_commands.CommandTree(SoupOverlord)

# init the spotipy
SPOTIFY_CLIENT = spotify_init.init_sp(const.CONFIG['spotify']['clientId'], const.CONFIG['spotify']['clientSecret'])


events.init_events(SoupOverlord, command_tree, SPOTIFY_CLIENT)
commands.init_commands(command_tree, SPOTIFY_CLIENT)


SoupOverlord.run(const.CONFIG['discord']['token'])
