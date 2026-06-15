import discord

from src.bot_core import SoupOverlordCore
from src.music_database import Track


class TrackInfoModal(discord.ui.Modal):
    def __init__(self, link: str, message: discord.Message, soup_overlord: SoupOverlordCore):
        super().__init__(
            title=f'Info for {link}'
        )
 
        self.link = link
        self.soup_overlord = soup_overlord
        self.message = message

        self.track_name = discord.ui.TextInput(
            label="Track name",
            style=discord.TextStyle.short,
            placeholder="e.g. Never Gonna Give You Up",
            required=True,
            max_length=100
        )

        self.track_author = discord.ui.TextInput(
            label="Track author",
            style=discord.TextStyle.short,
            placeholder="e.g. Rick Astley",
            required=True,
            max_length=100
        )

        self.add_item(self.track_name)
        self.add_item(self.track_author)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)

        track_name = self.track_name.value
        track_author = self.track_author.value

        entries = [entry for entry in self.soup_overlord.music_database.entries if entry.link == self.link]
        if len(entries) > 0:
            example = entries[0]
            
            await interaction.followup.send(
                f"This track is already recorded: `{example.track_name}` by `{example.track_author}` send by `{self.soup_overlord.get_cached_name(example.original_sender)}`", 
                ephemeral=True
            )

            print(example.created_at, self.message.created_at)
            if example.created_at != self.message.created_at:
                await self.message.add_reaction('♻️')
            
            return

        entries = self.soup_overlord.music_database.entries.copy()
        entries = [entry for entry in entries if entry.track_name == track_name]
        entries = [entry for entry in entries if entry.track_author == track_author]
        if len(entries) > 0:  # ideally there should be only 1 such entry
            example: Track = entries[0]

            if example.link is not None:
                await interaction.followup.send(
                    f"This track is already recorded: `{example.track_name}` by `{example.track_author}` send by `{self.soup_overlord.get_cached_name(example.original_sender)}`", 
                    ephemeral=True
                )
                
                if example.created_at != self.message.created_at:
                    await self.message.add_reaction('♻️')
                
                return
            
            example.update_link(self.link)

            response = f"Updated link for `{example.track_name}` by `{example.track_author}` sent by `{self.soup_overlord.get_cached_name(example.original_sender)}`. New link: `{self.link}`"
            await self.soup_overlord.discord_log(response)
            await interaction.followup.send(
                response,
                ephemeral=True
            )
            return

        self.soup_overlord.music_database.new_entry(track_name, track_author, self.link, self.message.author.id, self.message.created_at)
        await self.soup_overlord.discord_log(f"A new entry was added to the database: `{track_name}` by `{track_author}` sent by `{self.soup_overlord.get_cached_name(self.message.author.id)}`")

        await interaction.followup.send(
            content=f"Entered info for {self.link}: track name: `{track_name}`, track author: `{track_author}`, original_sender: `{self.soup_overlord.get_cached_name(self.message.author.id)}`",
            ephemeral=True
        )
        await self.message.add_reaction('⭐')


