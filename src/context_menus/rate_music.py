import discord
from discord.ext import commands as cmds
from discord import app_commands

from src.music_database import spotify_link_in_message, get_all_links_in_message, get_link_identifier
from src.ui.dropdown import RateMusicView

from src.bot_core import SoupOverlordCore



def register(soup_overlord: SoupOverlordCore):
    bot = soup_overlord
    music_database = soup_overlord.music_database

    async def rate_music(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer(ephemeral=True)

        if not spotify_link_in_message(message):
            await interaction.followup.send("This message does not contain a spotify link.")
            return
        
        link = get_link_identifier(get_all_links_in_message(message)[0])  # process only the first link, duh


        entries = music_database.filter(lambda entry: entry.link == link)

        # check if the track exists in the database
        if len(entries) == 0:
            await interaction.followup.send("Couldn't find the track. Please register it first")
            return

        if len(entries) > 1:
            await interaction.followup.send(f"Something went wrong. Please contact SoupOverlord maintainers with the following message: {link}")
            await soup_overlord.discord_log(f"Duplicate found for {link}")

        entry = entries[0]

        voter_id = interaction.user.id
        
        if voter_id == entry.original_sender:
            await interaction.followup.send("You can't vote on your own track")
            return
        
        old_vote = entry.votes[voter_id] if voter_id in entry.votes else None

        response = f'What would you rate `{entry.track_name}` by `{entry.track_author}` sent by `{soup_overlord.get_cached_name(entry.original_sender)}`?'  # TODO: turn original_sender into actual name
        if old_vote is not None:
            response += f" Your previous vote was `{old_vote}`."
        
        await interaction.followup.send(f'What would you rate `{entry.track_name}` by `{entry.track_author}`?', view=RateMusicView(entry, voter_id, soup_overlord))

    name = 'Rate music'
    rate_music_context_menu = app_commands.ContextMenu(
        name=name,
        callback=rate_music
    )
    bot.tree.add_command(rate_music_context_menu)
    soup_overlord.log(f"Registaring `{name}` app command")
