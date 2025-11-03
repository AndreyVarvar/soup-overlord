import discord
from discord.ext import commands as cmds

from utils import spotify_init
from utils import const

from src import events
from src import commands

# setup
intents = discord.Intents.all()
intents.message_content = True

SoupOverlord = cmds.Bot(intents=intents, command_prefix="$")

# init the spotipy
SPOTIFY_CLIENT = spotify_init.init_sp(const.CONFIG['spotify']['clientId'], const.CONFIG['spotify']['clientSecret'])


commands.init_commands(SoupOverlord, SPOTIFY_CLIENT)
events.init_events(SoupOverlord, SPOTIFY_CLIENT)


SoupOverlord.run(const.CONFIG['discord']['token'])
