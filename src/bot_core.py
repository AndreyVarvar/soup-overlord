import discord
from discord.ext import commands as cmds

from src.music_database import MusicDatabase

from src.const import CONFIG
from datetime import datetime, timezone


class SoupOverlordCore:
    def __init__(self) -> None:
        self.intents = discord.Intents.all()
        self.command_prefix = "S!"

        self.config = CONFIG

        self.bot = cmds.Bot(intents=self.intents, command_prefix=self.command_prefix, help_command=None)
        
        self.music_database = MusicDatabase()
        
    def run(self):
        self.bot.run(token=self.config["token"])
 
    def log(self, message, timestamp: bool = True, log_to_file: bool = False):
        current_time = datetime.now(timezone.utc).strftime("[UTC+0 %A %d, %B %Y, %H:%M:%S]: ")

        
        _log = ''
        if timestamp:
            _log += current_time
        _log += message
        
        if log_to_file:
            CURRENT_LOG_FILE = "logs/" + datetime.now(timezone.utc).strftime("%d.%m.%y")

            with open(CURRENT_LOG_FILE, "a") as file:
                file.write(_log + "\n")
        
        print(_log)

