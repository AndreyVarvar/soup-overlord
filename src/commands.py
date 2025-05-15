import discord
from discord.ext import commands
from utils import const
from utils.add_music import add_music


def init_commands(command_tree: discord.app_commands.CommandTree, spotify_client):
    @command_tree.context_menu(
        name='Add music',
        guild=discord.Object(id=const.SERVER_ID)
    )
    async def add_music_command(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer()
        code, response = await add_music(message, spotify_client)

        if code == 1:
            await interaction.followup.send("This message does not contain a spotify link.")
        elif code == -1:
            await interaction.followup.send("This track was already shared before!")
        elif code == 0:
            await interaction.followup.send(response)
            await message.add_reaction("<:confirmed:1291384088950997032>")  # make a visual cue everything is okay

        elif code == 2:
            await interaction.followup.send(response)


    @command_tree.command(
        name="echo",
        description="Repeast whatever you say",
        guild=discord.Object(id=const.SERVER_ID)
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
        guild=discord.Object(id=const.SERVER_ID)
    )
    async def help(interaction: discord.Interaction):
        await interaction.response.send_message("Just ask @andreyvarvar :P")

    @command_tree.command(
        name="ping",
        description="ping pong",
        guild=discord.Object(id=const.SERVER_ID)
    )
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")