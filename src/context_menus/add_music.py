import discord
from discord import app_commands

from src.music_database import spotify_link_in_message, get_all_links_in_message, get_link_identifier
from src.ui.modal import TrackInfoModal

from src.bot_core import SoupOverlordCore


def register(soup_overlord: SoupOverlordCore):
    bot = soup_overlord.bot

    async def add_music(interaction: discord.Interaction, message: discord.Message):
        if interaction.user.guild_permissions.administrator is False:
            await interaction.response.send_message("You need to be an administrator to execute this command.")
            return
 
        if not spotify_link_in_message(message):
            await interaction.followup.send("This message does not contain a spotify link")

        link = get_link_identifier(get_all_links_in_message(message)[0])

        # we now need to learn the name and the artist of this song
        # this is the part where it's required to be performed by a moderator
        await interaction.response.send_modal(TrackInfoModal(link, message.author.id, message, soup_overlord))

    add_music_context_menu = app_commands.ContextMenu(
        name='Add music',
        callback=add_music
    )
    bot.tree.add_command(add_music_context_menu)

