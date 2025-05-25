import discord
from utils import music_utils

class RateMusicDropdown(discord.ui.Select):
    def __init__(self, track_name, track_artist, voter):
        self.track_name = track_name
        self.track_artist = track_artist
        self.voter = voter

        options = [
            discord.SelectOption(
                label='1🤮',
                description='This music is TRASH, absolute GARBAGE, this should NOT EXIST'
            ),
            discord.SelectOption(
                label='2🤢',
                description='This is bad, I don\'t like it'
            ),
            discord.SelectOption(
                label='3😣',
                description='Could\'ve been worse, but definatelly could\'ve been better'
            ),
            discord.SelectOption(
                label='4😕',
                description='This track is not the best, but it\'s alright'
            ),
            discord.SelectOption(
                label='5🤨',
                description='Questionable, but overall it\'s ok'
            ),
            discord.SelectOption(
                label='6😤',
                description='This isn\'t all that bad, just not my taste'
            ),
            discord.SelectOption(
                label='7🤔',
                description='This is actually good'
            ),
            discord.SelectOption(
                label='8😳',
                description='This track is VERY good, but not perfect'
            ),
            discord.SelectOption(
                label='9😎',
                description='Awesome track, love it'
            ),
            discord.SelectOption(
                label='10🤩',
                description='THE BEST TRACK MY EARS EVER HEARD'
            ),
        ]

        super().__init__(
            placeholder='Rate this track',
            options=options,
            min_values=1,
            max_values=1
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        data = music_utils.database_fetch_info(self.track_name, self.track_artist)[0]

        name = data[0]
        artist = data[1]
        original_sender = data[2]

        if original_sender == self.voter:
            await interaction.followup.send("You can't vote on your own track", ephemeral=True)
            return

        vote = self.values[0][:-1]  # strip the emoji away (sadge)

        
        music_utils.database_update_votes_and_voters(name, artist, vote, self.voter)

        await interaction.followup.send(f'{self.values[0][:-1]} for `{self.track_name}` by `{self.track_artist}`', ephemeral=True)


class RateMusicView(discord.ui.View):
    def __init__(self, track_name, track_artist, voter):
        super().__init__()
        self.add_item(RateMusicDropdown(track_name, track_artist, voter))
