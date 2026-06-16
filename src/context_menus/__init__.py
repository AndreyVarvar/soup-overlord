from src.bot_core import SoupOverlordCore

from src.context_menus import add_music, rate_music, get_info


def init(soup_overlord: SoupOverlordCore):
    add_music.register(soup_overlord)
    rate_music.register(soup_overlord)
    get_info.register(soup_overlord)



