import discord
import spotipy
import sqlite3
from utils.log import log


SPOTIFY_LINK_IDENTIFIER = "https://open.spotify.com/track/"


def spotify_link_in_message(message: discord.Message):
    return SPOTIFY_LINK_IDENTIFIER in message.content


def get_all_links_in_message(message: discord.Message):
    links = []
    words = (' '.join(message.content.split('\n'))).split()
    for word in words:
        if SPOTIFY_LINK_IDENTIFIER in word:
            links.append(word)
    
    return links


def get_track(link: str, spotipy_client: spotipy.Spotify):
    try:
        return spotipy_client.track(link)
    except:
        return None
    

def get_track_info(track):
    name = track['name']
    artist = track['artists'][0]['name']  # we take the name of the first artist that shows up
    return name, artist


def database_fetch_info(name, artist):
    with sqlite3.connect("databases/spotify.sqlite") as connection:
        cursor = connection.cursor()
        select_query = "SELECT * FROM spotifies WHERE TrackName=? AND TrackAuthor=?;"
            
        data = cursor.execute(select_query, (name, artist)).fetchall()
    
    return data


def database_fetch_votes_and_voters(name, artist):
    data = database_fetch_info(name, artist)
    
    return data[0][5], data[0][6]


def database_fetch_all():
    with sqlite3.connect("databases/spotify.sqlite") as connection:
        cursor = connection.cursor()
        select_query = "SELECT * FROM spotifies;"

        data = cursor.execute(select_query).fetchall()
    
    return data


def database_fetch_original_sender(name, artist):
    data = database_fetch_info(name, artist)
    
    return data[0][2]



def database_update_votes_and_voters(name, artist, new_vote, new_voter):
    with sqlite3.connect("databases/spotify.sqlite") as connection:
        cursor = connection.cursor()
        select_query = "SELECT * FROM spotifies WHERE TrackName=? AND TrackAuthor=?;"
            
        data = cursor.execute(select_query, (name, artist)).fetchall()[0]
    
        votes = data[5]
        voters = data[6]


        if votes is None and voters is None:  # this track has no votes
            updated_votes = '' + new_vote
            updated_voters = '' + new_voter
            log(f'`{new_voter}` is the first voter for `{name}` by `{artist}`, rating it with a{"n" if new_vote=="8" else ""} `{new_vote}`')

        elif new_voter not in voters:  # the track has votes, but this person has not voted yet
            updated_votes += ' ' + new_vote
            updated_voters += ' ' + new_voter
            log(f'`{new_voter}` voted `{new_vote}` for `{name}` by `{artist}`')
        
        elif new_voter in voters:  # a person already voted on this track, so we just change an existing vote
            voter_index = voters.split().index(new_voter)
            
            v = votes.split()
            updated_votes = ' '.join(v[:voter_index] + [new_vote] + v[voter_index+1:])

            updated_voters = voters

            log(f'`{new_voter}` changed their vote with a{"n" if new_vote=="8" else ""} `{new_vote}` for `{name}` by `{artist}`')


        update_query = 'UPDATE spotifies SET Votes=?, Voters=? WHERE TrackName=? AND TrackAuthor=?'
        cursor.execute(update_query, (updated_votes, updated_voters, name, artist))


def track_in_database(name, artist):
    return len(database_fetch_info(name, artist)) > 0


def database_fetch_all_not_sent_by_user(username: str):
    with sqlite3.connect("databases/spotify.sqlite") as connection:
        cursor = connection.cursor()
        select_query = "SELECT * FROM spotifies WHERE OriginalSender!=?;"
            
        data = cursor.execute(select_query, (username,)).fetchall()
    return data



def spotify_get_track_link(entry, spotify_client):
    result = spotify_client.search(q=f"artist:{entry[1]} track:{entry[0]}")

    if len(result['tracks']['items']) == 0:  # spotify didn't find such a track - it probably got deleted
        return None

    return result['tracks']['items'][0]['external_urls']['spotify']



def database_fetch_all_alike(track_name: str, artist: str=None):
    with sqlite3.connect("databases/spotify.sqlite") as connection:
        cursor = connection.cursor()
        select_query: str
        args: tuple
        if artist is None:
            select_query = "SELECT * FROM spotifies WHERE UPPER(TrackName) LIKE UPPER(?)"
            args = ("%"+track_name+"%",)
        else:
            select_query = "SELECT * FROM spotifies WHERE UPPER(TrackName) LIKE UPPER(?) AND UPPER(TrackAuthor) LIKE UPPER(?)"
            args = ("%"+track_name+"%", "%"+artist+"%")
            
        data = cursor.execute(select_query, args).fetchall()
    
    return data


def make_embed(name: str, artist: str, original_sender: str, votes, voters):
    embed = discord.Embed(
        color=discord.Color.dark_gold(),
        title=f'Ratings for `{name}` by `{artist}`'
    )

    embed.set_author(name=original_sender)
        
    if len(votes) == 0:
        embed.set_footer(text='There are no votes for this track! Be the first one to rate it!')
    elif len(votes) == 1:
        embed.set_footer(text=f'A single rating of `{votes[0]}`')
    else:
        embed.set_footer(text=f'A total of `{len(votes)}` ratings, with an average of `{sum(votes)/len(votes):.2f}`')
    
    return embed
