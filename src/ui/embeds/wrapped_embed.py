import discord

from src.bot_core import SoupOverlordCore
from src.music_database import Track

import random

month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]


class WrappedShareCountEmbed(discord.Embed):
    # How many songs shared each month
    # How many tracks shared overall
    def __init__(self, soup_overlord: SoupOverlordCore, entries: list[Track], year: int):
        super().__init__()
        self.color = discord.Color.random()
        self.title = f'Tracks shared by month'

        track_shares_by_month = {i: 0 for i in range(12)}
        for entry in entries:
            track_shares_by_month[entry.created_at.month-1] += 1

        for i, month in enumerate(month_names):
            self.add_field(
                name=f"**{i+1})** *{month}*",
                value=f"-`{track_shares_by_month[i]}`-`{int(100 * track_shares_by_month[i]/len(entries))}%`-"
            )
        
        self.add_field(
            name="---------------------"*2,
            value="",
            inline=False
        )

        self.add_field(
            name=f"**Total tracks shared in `{year}`**",
            value=f"`{len(entries)}`"
        )

        self.set_footer(text=f'Wrapped-{year}')

    @classmethod
    async def build(cls, soup_overlord: SoupOverlordCore, entries: list[Track], year: int):
        return cls(
            soup_overlord,
            entries,
            year
        )


class WrappedMostPopularArtistEmbed(discord.Embed):
    # Most popular artist overall
    # Most popular artist by month
    def __init__(self, soup_overlord: SoupOverlordCore, entries: list[Track], year: int):
        super().__init__()

        self.color = discord.Color.random()
        self.title = f'Most shared artists'

        artists_by_month = {i: {} for i in range(12)}
        for entry in entries:
            if entry.track_author not in artists_by_month[entry.created_at.month-1]:
                artists_by_month[entry.created_at.month-1][entry.track_author] = 0

            artists_by_month[entry.created_at.month-1][entry.track_author] += 1


        for i, month in enumerate(month_names):
            if len(artists_by_month[i]) == 0:
                self.add_field(
                    name=f"**{i+1})** *{month}*",
                    value=f"*No tracks shared this month*",
                    inline=False
                )
                continue
                
            most_shared = max(artists_by_month[i], key=lambda x: artists_by_month[i][x])

            self.add_field(
                name=f"**{i+1})** *{month}*",
                value=f"-`{most_shared}`-`{artists_by_month[i][most_shared]} tracks`-",
                inline=False
            )

        self.add_field(
            name="---------------------"*2,
            value="",
            inline=False
        )

        artists = {}
        for entry in entries:
            if entry.track_author not in artists:
                artists[entry.track_author] = 0
            artists[entry.track_author] += 1

        artists = list(artists.items())
        artists.sort(key=lambda x: -x[1])

        top = 5  # how many to display
        self.add_field(
            name="Most shared artists:",
            value='\n'.join([f"{i+1}) `{artists[i][0]}` with `{artists[i][1]}` shares" for i in range(min(top, len(artists)))])
        )
        
        self.set_footer(text=f'Wrapped-{year}')

    @classmethod
    async def build(cls, soup_overlord: SoupOverlordCore, entries: list[Track], year: int):
        return cls(
            soup_overlord,
            entries,
            year
        )


class WrappedTopSharerEmbed(discord.Embed):
    # Leaderboard of who sent the most tracks
    # Top-music sender by month
    def __init__(self, soup_overlord: SoupOverlordCore, entries: list[Track], year: int, shared_most: discord.Member | discord.User):
        super().__init__()

        self.color = discord.Color.random()
        self.title = f'User activity'

        senders_by_month = {i: {} for i in range(12)}
        for entry in entries:
            if entry.original_sender not in senders_by_month[entry.created_at.month-1]:
                senders_by_month[entry.created_at.month-1][entry.original_sender] = 0

            senders_by_month[entry.created_at.month-1][entry.original_sender] += 1

        self.add_field(
            name="Most active sharers by month",
            value=""
        )

        for i, month in enumerate(month_names):
            if len(senders_by_month[i]) == 0:
                self.add_field(
                    name=f"**{i+1})** *{month}*",
                    value="*No tracks shared this month*",
                    inline=False
                )
                continue
            
            most_active = max(senders_by_month[i], key=lambda x: senders_by_month[i][x])

            self.add_field(
                name=f"**{i+1})** *{month}*",
                value=f"-`{soup_overlord.get_cached_name(most_active)}`-`{senders_by_month[i][most_active]} tracks`-",
                inline=False
            )

        self.add_field(
            name="---------------------"*2,
            value="",
            inline=False
        )

        shared_by_most_active = 0
        for month in senders_by_month:
            shared_by_most_active += senders_by_month[month][shared_most.id] if shared_most.id in senders_by_month[month] else 0

        self.add_field(
            name="User who shared the most:",
            value=f"`{soup_overlord.get_cached_name(shared_most.id)}`-`{shared_by_most_active} tracks shared`"
        )

        self.set_thumbnail(url=shared_most.avatar)
        
        self.set_footer(text=f'Wrapped-{year}')

    @classmethod
    async def build(cls, soup_overlord: SoupOverlordCore, entries: list[Track], year: int):
        senders = {}
        for entry in entries:
            if entry.original_sender not in senders:
                senders[entry.original_sender] = 0
            senders[entry.original_sender] += 1

        senders = list(senders.items())
        senders.sort(key=lambda x: -x[1])

        return cls(
            soup_overlord,
            entries,
            year,
            await soup_overlord.fetch_user(senders[0][0])
        )


class WrappedTopCriticEmbed(discord.Embed):
    # Top-rater
    def __init__(self, soup_overlord: SoupOverlordCore, year: int, rated_most: discord.Member | discord.User, total_rated: int):
        super().__init__()

        self.color = discord.Color.random()
        self.title = f'Top-rater'

        self.add_field(
            name="Top-critic:",
            value=f"`{soup_overlord.get_cached_name(rated_most.id)}`-`{total_rated} tracks rated`"
        )

        self.set_thumbnail(url=rated_most.avatar)
        
        self.set_footer(text=f'Wrapped-{year}')

    @classmethod
    async def build(cls, soup_overlord: SoupOverlordCore, entries: list[Track], year: int):
        raters = {}
        for entry in entries:
            for rater in entry.votes.keys():
                if rater not in raters:
                    raters[rater] = 0
                raters[rater] += 1

        raters = list(raters.items())
        raters.sort(key=lambda x: -x[1])

        return cls(
            soup_overlord,
            year,
            await soup_overlord.fetch_user(raters[0][0]),
            raters[0][1]
        )


class WrappedMostLovedTrackSendersEmbed(discord.Embed):
    # Most loved track senders
    def __init__(self, soup_overlord: SoupOverlordCore, entries: list[Track], year: int, most_loved: discord.Member | discord.User, other_loved: list[tuple[int, int]]):
        super().__init__()

        self.color = discord.Color.random()
        self.title = f'Most loved users'

        top = 3
        self.add_field(
            name="Most loved track senders:",
            value='\n'.join([f"{i+1}) `{soup_overlord.get_cached_name(other_loved[i][0])}` with `{other_loved[i][1]:.2f}` rating" for i in range(min(top, len(other_loved))) if other_loved[i][1] > 5.0])
        )

        self.set_thumbnail(url=most_loved.avatar)
        
        self.set_footer(text=f'Wrapped-{year}')

    @classmethod
    async def build(cls, soup_overlord: SoupOverlordCore, entries: list[Track], year: int):
        senders = {}
        for entry in entries:
            if entry.original_sender not in senders:
                senders[entry.original_sender] = [0, 0]
            senders[entry.original_sender][0] += len(entry.votes.values())
            senders[entry.original_sender][1] += sum(entry.votes.values())

        for sender in senders:
            senders[sender] = senders[sender][1] / senders[sender][0]  if senders[sender][0] != 0 else 0.0 # take average

        senders = list(senders.items())
        senders.sort(key=lambda x: -x[1])

        return cls(
            soup_overlord,
            entries,
            year,
            await soup_overlord.fetch_user(senders[0][0]),
            senders
        )


class WrappedMostLovedTracksEmbed(discord.Embed):
    # Most loved tracks
    def __init__(self, soup_overlord: SoupOverlordCore, entries: list[Track], year: int):
        super().__init__()

        self.color = discord.Color.random()
        self.title = f'Most loved tracks'

        tracks = [
            [
                entry, 
                (sum(entry.votes.values())/len(entry.votes.values())) if len(entry.votes.values()) > 0 else 0.0
            ] for entry in entries
        ]
        random.shuffle(tracks)
        tracks.sort(key=lambda x: -x[1])
        
        top = 10
        self.add_field(
            name="Most loved tracks:",
            value='\n'.join([f"{i+1}) `{tracks[i][0].track_name}` by `{tracks[i][0].track_author}` sent by `{soup_overlord.get_cached_name(tracks[i][0].original_sender)}` with rating `{tracks[i][1]:.2f}`" for i in range(min(top, len(tracks)))])
        )

        self.set_footer(text=f'Wrapped-{year}')

    @classmethod
    async def build(cls, soup_overlord: SoupOverlordCore, entries: list[Track], year: int):

        return cls(
            soup_overlord,
            entries,
            year
        )
