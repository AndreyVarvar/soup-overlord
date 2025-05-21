import discord
import spotipy
import sqlite3


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


        if voters is not None and new_voter in voters:
            return  # last line of defense against multiple votes from the same voter
        
        if votes is None:
            votes = ''

        votes += ' ' + new_vote


        if voters is None:
            voters = ''
    
        voters += ' ' + new_voter

        update_query = 'UPDATE spotifies SET Votes=?, Voters=? WHERE TrackName=? AND TrackAuthor=?'
        cursor.execute(update_query, (votes, voters, name, artist))
