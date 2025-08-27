import discord
from discord.ext import commands as cmds
from utils import const
from utils.log import log
from utils.special_channels import process_message_for_music

def init_events(bot: cmds.Bot, spotify_client):
    @bot.event
    async def on_ready():
        bot.tree.clear_commands(guild=discord.Object(id=int(const.CONFIG['discord']['guildID'])))
        await bot.tree.sync()
        await bot.tree.sync(guild=discord.Object(id=int(const.CONFIG['discord']['guildID'])))
        log("\n", timestamp=False)
        log("Bot startup")


    @bot.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return  # don't allow bots to trigger this event
        
        channel_id = message.channel.id
        if channel_id == const.CONFIG["server"]["musicChannel"]:
            await process_message_for_music(message, spotify_client)


    @bot.event
    async def on_command_error(ctx, error):
        print(error)
