import discord
from discord.ext import commands as cmds

from src.music_database import MusicDatabase

from src.const import CONFIG


class SoupOverlordCore:
    def __init__(self) -> None:
        self.intents = discord.Intents.all()
        self.command_prefix = "S!"

        self.bot = cmds.Bot(intents=self.intents, command_prefix=self.command_prefix, help_command=None)
        self.token = CONFIG["token"]
        
        self.music_database = MusicDatabase()
        
    def run(self):
        self.bot.run(token=self.token)

