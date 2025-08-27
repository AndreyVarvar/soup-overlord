import sqlite3
from .log import log
import discord
import spotipy

from .music_utils import spotify_link_in_message, get_all_links_in_message, get_track, get_track_info


RESPONSES = [
    "No spotify link in message.",
    "No such track."
]

async def add_music_to_database(message: discord.Message, spotipy_client: spotipy.Spotify):
    """
    STEP 1: verify, that the message contains a spotify link
    STEP 2: verify, that the song/music exists on spotify
    STEP 3: check, if this track was shared before
    STEP 4: add the track to the spotify database
    """

    # step 1
    if not spotify_link_in_message(message):
        return [1, RESPONSES[0]]  # no need to go further, this is a normal message (we hope)
    
    # step 2
    links = get_all_links_in_message(message)

    # step 3
    response = [2, ""]  # prepare a response ahead of time

    with sqlite3.connect("databases/spotify.sqlite") as connection:
        cursor = connection.cursor()
        select_query = "SELECT * FROM spotifies WHERE TrackName=? AND TrackAuthor=?;"

        for link in links:
            track = get_track(link, spotipy_client)

            if track is None:
                response[1] += f"Track `{link}` does not exist." + "\n"
                continue

            name, artist = get_track_info(track)
            
            data = cursor.execute(select_query, (name, artist)).fetchall()

            if len(data) > 0:
                response[1] += f"Track `{name}` by `{artist}` was shared before!" + "\n"
                continue # this track is already in the database
    
        # step 4
            cursor.execute(
                "INSERT INTO spotifies (TrackName, TrackAuthor, OriginalSender, createdAt, updatedAt, Votes, Voters) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                (name, artist, message.author.name, str(message.created_at), str(message.created_at), None, None)
            )

            log(f"Added `{name}` by `{artist}` to the music database.")
            response[0] = 0
            response[1] += f"Track `{name}` by `{artist}` was successfully added to the database." + "\n"

    return response