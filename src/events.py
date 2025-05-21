import discord
from utils import const
from utils.log import log
from utils.special_channels import process_message_for_music

def init_events(client, command_tree, spotify_client):
    @client.event
    async def on_ready():
        await command_tree.sync(guild=discord.Object(id=const.CONFIG["server"]["id"]))
        log("\n", timestamp=False)
        log("Bot startup")

    @client.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return  # don't allow bots to trigger this event
        

        channel_id = message.channel.id

        if channel_id == const.CONFIG["server"]["musicChannel"] or ("DEBUGGING" in message.content):
            await process_message_for_music(message, spotify_client)

    @client.event
    async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
        # print(f"{user.name} reacted with {reaction.emoji}")
        pass
    