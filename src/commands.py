import discord
from utils import const
from utils.add_music import add_music


def init_commands(command_tree, spotify_client):
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