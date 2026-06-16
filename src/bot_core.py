import discord
from discord.ext import commands as cmds

from src.music_database import MusicDatabase

from src.const import CONFIG
from datetime import datetime, timezone

import json


class SoupOverlordCore(cmds.Bot):
    def __init__(self) -> None:
        self.command_prefix = "S!"

        self.config = CONFIG
        
        super().__init__(
            intents=discord.Intents.all(),
            command_prefix=self.command_prefix
        )
        self.remove_command('help')
        self.music_database = MusicDatabase()
        
    def run(self):
        super().run(token=self.config["token"])

    async def discord_log(self, message):
        channel = self.get_channel(self.config["discordServer"]["logChannelID"])
        if channel is None:
            channel = await self.fetch_channel(self.config["discordServer"]["logChannelID"])

        if channel is None:
            self.log(f"Couldn't find channel: {self.config["discordServer"]["logChannelID"]}")
            return

        await channel.send(message)

    def log(self, message, timestamp: bool = True, log_to_file: bool = False):
        current_time = datetime.now(timezone.utc).strftime("[UTC+0 %A %d, %B %Y, %H:%M:%S]: ")
        
        _log = ''
        if timestamp:
            _log += current_time
        _log += message
        
        if log_to_file:
            log_file = "logs/" + datetime.now(timezone.utc).strftime("%d.%m.%y")

            with open(log_file, "a") as file:
                file.write(_log + "\n")
        
        print(_log)
    
    def get_cached_name(self, user_id: int):
        """
        1) They are on the server and their name matched the one in cache
        2) They are on the server but they changed their name
        3) They are not on the server so their old name is used
        """

        with open("username_cache.json", "r") as file:
            cache = json.load(file)

        if str(user_id) in cache:
            return cache[str(user_id)]

        user = self.get_user(user_id)
        if user is None:
            user = self.fetch_user(user_id)

        if user is None:
            return "Unknown User"


        cache[str(user_id)] = user.display_name  # update/set their nickname on the server

        with open("username_cache.json", "w") as file:
            json.dump(cache, file, indent=4)

        return cache[str(user_id)]
