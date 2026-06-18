import discord

from src.music_database import Track, get_link_from_identifier
from src.bot_core import SoupOverlordCore

from src.utils import average


class InfoEmbed(discord.Embed):
    def __init__(
        self, 
        original_sender: discord.User | discord.Member,  # the person who shared the track
        soup_overlord: SoupOverlordCore, 
        entry: Track,
        sender: discord.User | discord.Member  # the person who is curious about the track
    ):
        super().__init__()
        
        self.color = discord.Color.dark_gold()

        self.set_author(
            name=f"Sent by: {soup_overlord.get_cached_name(entry.original_sender)}",
            icon_url=original_sender.avatar
        )
        
        self.add_field(
            name="Track name",
            value=entry.track_name,
            inline=True
        )
        
        self.add_field(
            name="Track author",
            value=entry.track_author,
            inline=True
        )

        votes_info = ""
        if len(entry.votes) == 0:
            votes_info = "No votes"
        else:
            votes_info = f"{average(list(entry.votes.values())):.2f}"
    
        self.add_field(
            name="Average rating",
            value=votes_info,
            inline=True
        )

        self.add_field(
            name="Total votes",
            value=str(len(entry.votes)),
            inline=True
        )

        self.add_field(
            name="Link to track",
            value=f"[**spotify.com**]({get_link_from_identifier(entry.link)})"
        )

        if entry.original_sender != sender.id:
            self.add_field(
                name="My vote",
                value=entry.votes[sender.id] if sender.id in entry.votes else "Did not vote",
                inline=True
            )

        self.add_field(
            name="Share date",
            value=f"{entry.created_at.strftime('%B %d, %Y')}"
        )

    @classmethod
    async def build(cls, soup_overlord: SoupOverlordCore, entry: Track, sender: discord.User | discord.Member):
        original_sender = await soup_overlord.fetch_user(entry.original_sender)

        return cls(
            original_sender,
            soup_overlord,
            entry,
            sender
        )
