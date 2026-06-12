from src.bot_core import SoupOverlordCore

import src.events as events
import src.commands as commands
import src.context_menus as context_menus

"""
A place to bring everything together. It's where we assemble the pieces of the bot into one.
"""

class SoupOverlord(SoupOverlordCore):
    def __init__(self) -> None:
        super().__init__()

        events.init(self)
        commands.init(self)
        context_menus.init(self)


