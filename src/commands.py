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

        embed = music_utils.make_embed(name, artist, original_sender, votes, voters)
        
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
            await interaction.followup.send("WOW, there isn\'t a single track that doesn\'t have your vote!")
        else:
            link = None
            k = len(data)
            for i in range(k):  # list through all possible items and find the one, that works
                random_item = random.choice(data)
                link = music_utils.spotify_get_track_link(random_item, spotify_client)

                if link is None:  # no such track exists on spotify end
                    del data[data.index(random_item)]

                    if len(data) == 0:
                        break
                    else:
                        continue
                else:
                    break

            if link is None:
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
        name="get-least-rated",
        description="Rate a track you know the name of",
        guild=discord.Object(id=const.CONFIG["server"]["id"])
    )
    async def get_least_rated(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        data = music_utils.database_fetch_all_not_sent_by_user(interaction.user.name)
        least_rated = data[0]
        least_votes = len(least_rated[5].split())
        similarly_voted = [least_rated]

        for item in data[1:]:
            votes = len(item[5].split())
            if votes < least_votes:
                least_votes = votes
                least_rated = item
                similarly_voted.clear()
                similarly_voted.append(least_rated)
            elif votes == least_votes:
                similarly_voted.append(item)

        link = None
        least_voted_track: tuple

        while len(similarly_voted) > 0:
            least_voted_track = random.choice(similarly_voted)
            if interaction.user.name in least_voted_track[6]:
                del similarly_voted[similarly_voted.index(least_voted_track)]
                continue

            link = music_utils.spotify_get_track_link(least_voted_track, spotify_client)
            if link is not None:
                break
            else:
                del similarly_voted[similarly_voted.index(least_voted_track)]

        if link is not None:
            await interaction.followup.send(f"Rate `{least_voted_track[0]}` by `{least_voted_track[1]}` with just `{least_votes}` votes?\n{link}", view=RateMusicView(least_voted_track[0], least_voted_track[1], interaction.user.name))
        else:
            await interaction.followup.send("WOW, there isn't a single track without your vote!")



    @command_tree.command(
        name="rate-specific-track",
        description="Rate a track you know the name of",
        guild=discord.Object(id=const.CONFIG["server"]["id"])
    )
    async def rate_specific(interaction: discord.Interaction, track_name: str, track_artist: str=None):
        await interaction.response.defer(ephemeral=True)
        
        data = music_utils.database_fetch_all_alike(track_name, track_artist)
        entries: list

        if len(track_name) <= 3:  # in this case, we only search track that are 3 characters or less in length
            # remove all tracks with 4 or more characters in their name
            entries = []
            for i in data:
                if len(i[0]) <= 3:
                    entries.append(i)
            
        else:
            entries = data
        
        if len(entries) == 0:
            await interaction.followup.send("No track with such a name was found")
        elif len(entries) == 1:
            entry = entries[0]
            link = music_utils.spotify_get_track_link(entry, spotify_client)

            user_vote = None
            if interaction.user.name in entry[6]:
                votes = entry[5].split()
                voters = entry[6].split()
                user_vote = votes[voters.index(interaction.user.name)]

            if link is not None:
                user_vote_text = ("\nYour previous vote was: " + str(user_vote)) if user_vote is not None else ("")
                await interaction.followup.send(f'What would you rate `{entry[0]}` by `{entry[1]}`?{user_vote_text}\n{link}', view=RateMusicView(entry[0], entry[1], interaction.user.name))
            else:
                await interaction.followup.send("No track with such a name was found")
        elif len(entries) < 4:
            responses = []
            for entry in entries:
                responses.append(f"- Track `{entry[0]}` by `{entry[1]}` sent by `{entry[2]}`")
            
            response = f"There are a total of {len(entries)} entries that match your result:\n" + '\n'.join(responses) + "\nPlease use this command again, but with a specific artist specified."
            await interaction.followup.send(response)
        else:
            await interaction.followup.send(f"Search query is too vague, there are multiple tracks with similar names ({len(entries)} entries found)")


    @command_tree.command(
        name="get-rating-of-specific-track",
        description="Get a rating of a track in the database",
        guild=discord.Object(id=const.CONFIG["server"]["id"])
    )
    async def get_rating_of_track(interaction: discord.Interaction, track_name: str, track_artist: str=None):
        await interaction.response.defer(ephemeral=True)
        
        data = music_utils.database_fetch_all_alike(track_name, track_artist)
        entries: list

        if len(track_name) <= 3:  # in this case, we only search track that are 3 characters or less in length
            # remove all tracks with 4 or more characters in their name
            entries = []
            for i in data:
                if len(i[0]) <= 3:
                    entries.append(i)
            
        else:
            entries = data
        
        if len(entries) == 0:
            await interaction.followup.send("No track with such a name was found")
        elif len(entries) == 1:
            entry = entries[0]
            
            embed = music_utils.make_embed(entry[0], entry[1], entry[2], entry[5].split(), entry[6].split())
        
            await interaction.followup.send(embed=embed)
        elif len(entries) < 4:
            responses = []
            for entry in entries:
                responses.append(f"- Track `{entry[0]}` by `{entry[1]}` sent by `{entry[2]}`")
            
            response = f"There are a total of {len(entries)} entries that match your result:\n" + '\n'.join(responses) + "\nPlease use this command again, but with a specific artist specified."
            await interaction.followup.send(response)
        else:
            await interaction.followup.send(f"Search query is too vague, there are multiple tracks with similar names ({len(entries)} entries found)")



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
        name="get-total-unvoted",
        description="Shows how many entries you have not voted on yet",
        guild=discord.Object(id=const.CONFIG["server"]["id"])
    )
    async def get_total_unvoted(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        entries = music_utils.database_fetch_all_not_sent_by_user(interaction.user.name)
        total_unvoted = 0
        for entry in entries:
            if entry[6] is None:
                total_unvoted += 1
                continue
            if interaction.user.name not in entry[6]:
                total_unvoted += 1
        
        if total_unvoted == 0:
            await interaction.followup.send("You have voted on every single track.")
        else:
            await interaction.followup.send(f"You have {total_unvoted} total unvoted track{'' if total_unvoted == 1 else 's'}")


    @command_tree.command(
        name="fetch-database-volume",
        description="Shows how many tracks are in the database",
        guild=discord.Object(id=const.CONFIG["server"]["id"])
    )
    async def fetch_database_volume(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        data = music_utils.database_fetch_all()
        amount = len(data)

        await interaction.followup.send(f"There are currently a total of {amount} entires in the database.")


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
