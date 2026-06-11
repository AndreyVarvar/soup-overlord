import discord
from src.music_database import MusicDatabase, Track

class RateMusicDropdown(discord.ui.Select):
    def __init__(self, entry: Track, voter: int):
        self.entry = entry
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

        if self.entry.original_sender == self.voter:
            await interaction.followup.send("You can't vote on your own track.", ephemeral=True)
            return

        old_vote = self.entry.get_vote_by(self.voter)
        new_vote = int(self.values[0][:-1])  # strip the emoji away (sadge)

        self.entry.update_vote_by(self.voter, new_vote)

        response = f'{new_vote} for `{self.entry.track_name}` by `{self.entry.track_author}`.'
        if old_vote is not None:
            response += f' Previous vote was `{old_vote}`'

        await interaction.followup.send(response, ephemeral=True)


class RateMusicView(discord.ui.View):
    def __init__(self, entry: Track, voter: int):
        super().__init__()
        self.add_item(RateMusicDropdown(entry, voter))
