from discord.ext import commands as cmds
from src.music_database import MusicDatabase

from src.bot_core import SoupOverlordCore

from src.log import log

from . import \
    music_random_unrated, \
    test, \
    music_get_least_rated, \
    music_rate_specific, \
    echo, \
    help, \
    music_unrated_count, \
    music_get_rating_of, \
    music_total, \
    ping


def init(soup_overlord: SoupOverlordCore):
    log("Registering commands.")

    # general stuff
    echo.register(soup_overlord)
    help.register(soup_overlord)
    test.register(soup_overlord)
    ping.register(soup_overlord)
    
    # music related stuff
    music_random_unrated.register(soup_overlord)
    music_get_least_rated.register(soup_overlord)
    music_rate_specific.register(soup_overlord)
    music_unrated_count.register(soup_overlord)
    music_get_rating_of.register(soup_overlord)
    music_total.register(soup_overlord)


