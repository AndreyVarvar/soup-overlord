import discord
from discord import app_commands

from src.music_database import spotify_link_in_message, get_all_links_in_message, get_link_identifier
from src.ui.embeds.info_embed import InfoEmbed

from src.bot_core import SoupOverlordCore



def register(soup_overlord: SoupOverlordCore):
    bot = soup_overlord
    music_database = soup_overlord.music_database

    async def get_info(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer(ephemeral=True)

        if not spotify_link_in_message(message):
            await interaction.followup.send("This message is not a spotify link")
            return
        
        link = get_link_identifier(get_all_links_in_message(message)[0])

        entries = music_database.filter(lambda entry: entry.link == link)

        if len(entries) == 0:
            await interaction.followup.send("Add this track to the database first using 'Add music' before getting a rating")
            return

        entry = entries[0]

        sender = interaction.user

        await interaction.followup.send(embed=await InfoEmbed.build(soup_overlord, entry, sender))


    get_rating_context_menu = app_commands.ContextMenu(
        name='Get info',
        callback=get_info
    )
    bot.tree.add_command(get_rating_context_menu)
