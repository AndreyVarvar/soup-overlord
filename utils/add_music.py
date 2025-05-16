import sqlite3
from .log import log
import discord
import spotipy

SPOTIFY_LINK_IDENTIFIER = "https://open.spotify.com/track/"

RESPONSES = [
    "No spotify link in message.",
    "No such track."
]

async def add_music(message: discord.Message, spotipy_client: spotipy.Spotify):
    """
    STEP 1: verify, that the message contains a spotify link
    STEP 2: verify, that the song/music exists on spotify
    STEP 3: check, if this track was shared before
    STEP 4: add the track to the spotify database
    """
    # step 1
    if SPOTIFY_LINK_IDENTIFIER not in message.content:
        return [1, RESPONSES[0]]  # no need to go further, this is a normal message (we hope)
    
    # step 2
    links = []
    singular_words = (' '.join(message.content.split('\n'))).split()
    for s in singular_words:
        if SPOTIFY_LINK_IDENTIFIER in s:
            links.append(s)
    

    # step 3
    response = [2, ""]

    with sqlite3.connect("databases/spotify.sqlite") as connection:
        cursor = connection.cursor()
        select_query = "SELECT * FROM spotifies WHERE TrackName=? AND TrackAuthor=?;"
        for link in links:

            try:
                track = spotipy_client.track(link)
            except:
                response[1] += f"Track `{link.split(SPOTIFY_LINK_IDENTIFIER)[1]}` does not exist." + "\n"
                continue

            name = track['name']
            artist = track['artists'][0]['name']  # we take the name of the first artist that shows up
            
            data = cursor.execute(select_query, (name, artist)).fetchall()

            if len(data) > 0:
                response[1] += f"Track `{name}` by `{artist}` was shared before!" + "\n"
                continue # this track is already in the database
    
        # step 4
            cursor.execute(
                "INSERT INTO spotifies (TrackName, TrackAuthor, OriginalSender, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?)", 
                (name, artist, message.author.name, str(message.created_at), str(message.created_at))
            )

            log(f"Added `{name}` by `{artist}` to the music database.")
            response[0] = 0
            response[1] += f"Track `{name}` by `{artist}` was successfully added to the database." + "\n"

    return response