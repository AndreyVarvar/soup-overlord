import discord
from discord.ext import commands
from utils import const
from utils.add_music import add_music_to_database
from utils import music_utils
from ui.dropdown import RateMusicView


def init_commands(command_tree: discord.app_commands.CommandTree, spotify_client):
    @command_tree.context_menu(
        name='Add music',
        guild=discord.Object(id=const.CONFIG["server"]["id"])
    )
    async def add_music(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer(ephemeral=True)
        code, response = await add_music_to_database(message, spotify_client)

        if code == 1:
            await interaction.followup.send("This message does not contain a spotify link.")
        elif code == -1:
            await interaction.followup.send("This track was already shared before!")
        elif code == 0:
            await interaction.followup.send(response)
            await message.add_reaction("<:confirmed:1291384088950997032>")  # make a visual cue everything is okay

        elif code == 2:
            await interaction.followup.send(response)

    
    @command_tree.context_menu(
        name='Rate music',
        guild=discord.Object(id=const.CONFIG["server"]["id"])
    )
    async def rate_music(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer(ephemeral=True)

        if not music_utils.spotify_link_in_message(message):
            await interaction.followup.send("This message is not a spotify link.")
            return
        
        link = music_utils.get_all_links_in_message(message)[0]  # process only the first link, duh

        track = music_utils.get_track(link, spotify_client)

        if track is None:
            await interaction.followup.send("This spotify track does not exist.")
            return

        name, artist = music_utils.get_track_info(track)
        votes, voters = music_utils.database_fetch_votes_and_voters(name, artist)

        original_sender = music_utils.database_fetch_original_sender(name, artist)

        voter = interaction.user.name

        if voters is not None and voter in voters:
            await interaction.followup.send("You already voted on this track")
            return
        
        if voter == original_sender:
            await interaction.followup.send("You can't vote on your own track")
            return
        
        await interaction.followup.send(f'What would you rate `{name}` by `{artist}`?', view=RateMusicView(name, artist, voter))




    @command_tree.command(
        name="echo",
        description="Repeast whatever you say",
        guild=discord.Object(id=const.CONFIG["server"]["id"])
    )
    @commands.is_owner()
    async def echo(interaction: discord.Interaction, message: str, channel: discord.channel.TextChannel=None):
        await interaction.response.send_message("Used echo", ephemeral=True)

        if channel is not None:
            await channel.send(message)
        else:
            await interaction.channel.send(message)
    
    @command_tree.command(
        name="help",
        description="Get general information about the bot",
        guild=discord.Object(id=const.CONFIG["server"]["id"])
    )
    async def help(interaction: discord.Interaction):
        await interaction.response.send_message("Just ask @andreyvarvar :P")

    @command_tree.command(
        name="ping",
        description="ping pong",
        guild=discord.Object(id=const.CONFIG["server"]["id"])
    )
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")