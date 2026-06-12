import discord

from src.bot_core import SoupOverlordCore

import emoji


class TrackInfoModal(discord.ui.Modal):
    def __init__(self, link: str, sender_id: int, message: discord.Message, soup_overlord: SoupOverlordCore):
        super().__init__(
            title=f'Info for {link}'
        )
 
        self.link = link
        self.sender_id = sender_id
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
        track_name = self.track_name.value
        track_author = self.track_author.value

        entries = self.soup_overlord.music_database.entries.copy()

        entries = [entry for entry in entries if entry.track_name == track_name]
        entries = [entry for entry in entries if entry.track_author == track_author]
        # entries = [entry for entry in entries if entry.link == self.link]  # temorarily down

        if len(entries) > 0:  # ideally there should be only 1 such entry
            example = entries[0]
            await interaction.response.send_message(
                f"This track is already recorded: `{example.track_name}` by `{example.track_author}` send by `{self.soup_overlord.get_cached_name(example.original_sender)}`", 
                ephemeral=True
            )
            
            if example.created_at != self.message.created_at:
                await self.message.add_reaction('♻️')
            
            return

        self.soup_overlord.music_database.new_entry(track_name, track_author, self.link, self.sender_id)
        await self.soup_overlord.discord_log(f"A new entry was added to the database: `{track_name}` by `{track_author}` sent by `{self.soup_overlord.get_cached_name(self.sender_id)}`")

        await interaction.response.send_message(
            content=f"Entered info for {self.link}: track name: `{track_name}`, track author: `{track_author}`, original_sender: `{self.soup_overlord.get_cached_name(self.sender_id)}`",
            ephemeral=True
        )
        await self.message.add_reaction('⭐')


