import discord

from src.music_database import Track
from src.bot_core import SoupOverlordCore


def make_music_rating_embed(entry: Track, soup_overlord: SoupOverlordCore):
    embed = discord.Embed(
        color=discord.Color.dark_gold(),
        title=f'Ratings for `{entry.track_name}` by `{entry.track_author}`'
    )

    embed.set_author(name=soup_overlord.get_cached_name(entry.original_sender))
        
    if len(entry.votes) == 0:
        embed.set_footer(text='There are no votes for this track! Be the first one to rate it!')
    else:
        embed.set_footer(text=f'A total of `{len(entry.votes)}` ratings, with an average of `{sum(entry.votes.values())/len(entry.votes):.2f}`')
    
    return embed
