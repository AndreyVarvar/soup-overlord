import discord
from discord.ext import commands
from utils import const
from utils.add_music import add_music_to_database
from utils import music_utils
from ui.dropdown import RateMusicView
import spotipy
import random



def init_commands(command_tree: discord.app_commands.CommandTree, spotify_client: spotipy.Spotify):
    init_context_menu_commands(command_tree, spotify_client)
    init_slash_commands(command_tree, spotify_client)



def init_context_menu_commands(command_tree: discord.app_commands.CommandTree, spotify_client):
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
            await message.add_reaction('\u2B50')  # make a visual cue everything is okay

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

        # check if the track exists in the database
        if not music_utils.track_in_database(name, artist):
            await interaction.followup.send("Add the track to the database first. Use 'Add music' for that")
            return

        original_sender = music_utils.database_fetch_original_sender(name, artist)

        voter = interaction.user.name
        
        if voter == original_sender:
            await interaction.followup.send("You can't vote on your own track")
            return
        
        await interaction.followup.send(f'What would you rate `{name}` by `{artist}`?', view=RateMusicView(name, artist, voter))




    @command_tree.context_menu(
        name='Get rating',
        guild=discord.Object(id=const.CONFIG["server"]["id"])
    )
    async def get_rating(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer(ephemeral=True)

        if not music_utils.spotify_link_in_message(message):
            await interaction.followup.send("This message is not a spotify link")
            return
        
        link = music_utils.get_all_links_in_message(message)[0]

        track = music_utils.get_track(link, spotify_client)

        if track is None:
            await interaction.followup.send("This track has no ratings because it doesn't even exist")
            return

        name, artist = music_utils.get_track_info(track)

        if not music_utils.track_in_database(name, artist):
            await interaction.followup.send("Add this track to the database first using 'Add music' before getting a rating")
            return

        votes, voters = music_utils.database_fetch_votes_and_voters(name, artist)
        votes = list(map(int, votes.split())) if votes is not None else []
        voters = voters.split() if voters is not None else []

        original_sender = music_utils.database_fetch_original_sender(name, artist)

        embed = discord.Embed(
            color=discord.Color.dark_gold(),
            title=f'Ratings for `{name}` by `{artist}`'
        )

        embed.set_author(name=original_sender)
        
        if len(votes) == 0:
            embed.set_footer(text='There are no votes for this track! Be the first one to rate it!')
        elif len(votes) == 1:
            embed.set_footer(text=f'A single rating of `{votes[0]}` by `{voters[0]}`')
        else:
            embed.set_footer(text=f'A total of `{len(votes)}` ratings, with an average of `{sum(votes)/len(votes):.2f}`')
        
        await interaction.followup.send(embed=embed)



def init_slash_commands(command_tree: discord.app_commands.CommandTree, spotify_client: spotipy.Spotify):
    @command_tree.command(
        name="music-rate-random",
        description="Get a random track to rate",
        guild=discord.Object(id=const.CONFIG["server"]["id"])
    )
    async def music_rate_random(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        data = music_utils.database_fetch_all_not_sent_by_user(interaction.user.name)

        if len(data) == 0:
            await interaction.followup.send("Sadly, there are no tracks for you to vote on")

        # clean up the data a little
        new_data = []
        for i in range(len(data)):
            item = data[i]
            if item[6] is None or interaction.user.name not in item[6]:
                new_data.append(item)
        
        data = new_data
        
        if len(data) == 0:
            await interaction.followup.send("WOW, there isn't a single track that doesn't have your vote!")
        else:
            link = ''
            for i in range(len(data)):  # list through all possible items and find the one, that works
                random_item = random.choice(data)
                result = spotify_client.search(q=f"artist:{random_item[1]} track:{random_item[0]}")

                if len(result['tracks']['items']) == 0:  # spotify didn't find such a track - it probably got deleted
                    del data[data.index(random_item)]

                    if len(data) == 0:
                        break
                    else:
                        continue

                link = result['tracks']['items'][0]['external_urls']['spotify']
                break

            if len(link) == 0:
                await interaction.followup.send('WOW, there isn\'t a single track that doesn\'t have your vote!')
            else:
                await interaction.followup.send(f'What would you rate `{random_item[0]}` by `{random_item[1]}`?\n{link}', view=RateMusicView(random_item[0], random_item[1], interaction.user.name))
    



    @command_tree.command(
        name="test",
        description="test",
        guild=discord.Object(id=const.CONFIG["server"]["id"])
    )
    @commands.is_owner()
    async def test(interaction: discord.Interaction):
        track = spotify_client.search(q="artist:405Okced track:Staff Roll")
        print(track)
        await interaction.response.send_message('test successful')
    




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