import discord

from src.bot_core import SoupOverlordCore


def register(soup_overlord: SoupOverlordCore):
    soup_overlord.log("Registering 'on-ready' event.")
    
    bot = soup_overlord.bot

    @bot.event
    async def on_ready():
        bot.tree.clear_commands(guild=discord.Object(id=int(soup_overlord.config["discordServer"]['serverID'])))
        await bot.tree.sync()
        await bot.tree.sync(guild=discord.Object(id=int(soup_overlord.config["discordServer"]['serverID'])))
        
        soup_overlord.log("\n", timestamp=False)
        soup_overlord.log("Bot startup")

        await soup_overlord.discord_log("Woke up!")
