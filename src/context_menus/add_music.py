import discord
from discord import app_commands

from src.music_database import spotify_link_in_message, get_all_links_in_message, get_link_identifier
from src.ui.modal import TrackInfoModal

from src.bot_core import SoupOverlordCore


def register(soup_overlord: SoupOverlordCore):
    bot = soup_overlord
    music_database = soup_overlord.music_database

    async def add_music(interaction: discord.Interaction, message: discord.Message):
        if interaction.user.guild_permissions.administrator is False:
            await interaction.response.send_message(
                "You need to be an administrator to execute this command.",
                ephemeral=True
            )
            return
 
        if not spotify_link_in_message(message):
            await interaction.response.send_message(
                "This message does not contain a spotify link",
                ephemeral=True
            )

        link = get_link_identifier(get_all_links_in_message(message)[0])

        # check if the link is already in the database
        entries = music_database.filter(lambda entry: entry.link == link)
        if len(entries) > 0:
            example = entries[0]

            await interaction.response.send_message(
                f"This track is already recorded: `{example.track_name}` by `{example.track_author}` send by `{soup_overlord.get_cached_name(example.original_sender)}`", 
                ephemeral=True
            )
            
            if example.created_at != message.created_at:
                await message.add_reaction('♻️')
            
            return

        # we now need to learn the name and the artist of this song
        # this is the part where it's required to be performed by a moderator
        await interaction.response.send_modal(TrackInfoModal(link, message, soup_overlord))

    name = 'Add music'
    add_music_context_menu = app_commands.ContextMenu(
        name=name,
        callback=add_music
    )
    bot.tree.add_command(add_music_context_menu)

    soup_overlord.log(f"Registering `{name}` app command")
