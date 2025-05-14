import sqlite3
from .log import log
import discord

SPOTIFY_LINK_IDENTIFIER = "https://open.spotify.com/track/"
RESPONSES = [
    "No spotify link in message.",
    "No such track."
]

async def add_music(message: discord.Message, spotipy_client):
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
    
    names: list[str] = []
    artists: list[str] = []
    for link in links:
        try:
            track = spotipy_client.track(link)
        except:
            return [-1, RESPONSES[1]]

        names.append(track['name'])
        artists.append(track['artists'][0]['name'])  # we take the name of the first artist that shows up

    # step 3
    response = [2, ""]

    with sqlite3.connect("databases/spotify.sqlite") as connection:
        cursor = connection.cursor()
        select_query = "SELECT * FROM spotifies WHERE TrackName=? AND TrackAuthor=?;"
        for i in range(len(names)):
            data = cursor.execute(select_query, (names[i], artists[i])).fetchall()

            if len(data) > 0:
                response[1] += f"Track `{names[i]}` by `{artists[i]}` was shared before!" + "\n"
                continue # this track is already in the database
    
        # step 4
            cursor.execute(
                "INSERT INTO spotifies (TrackName, TrackAuthor, OriginalSender, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?)", 
                (names[i], artists[i], message.author.name, str(message.created_at), str(message.created_at))
            )

            log(f"Added `{names[i]}` by `{artists[i]}` to the music database.")
            response[0] = 0
            response[1] += f"Track `{names[i]}` by `{artists[i]}` was successfully added to the database." + "\n"

    return response