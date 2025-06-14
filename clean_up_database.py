import spotipy
from utils.spotify_init import init_sp
from utils import const
import sqlite3
from utils.log import log


def clean_up_database(spotify_client: spotipy.Spotify):
    """
        Over time some tracks get deleted from spotify database.
        We iterate over each track and check if it still exists on the spotify side.
        If not, we permanently delete it from our spotify database. 
    """
    with sqlite3.connect("databases/spotify.sqlite") as connection:
        cursor = connection.cursor()
        select_query = "SELECT * FROM spotifies"
                    
        data = cursor.execute(select_query).fetchall()

        delete_query = "DELETE FROM spotifies WHERE TrackName=? AND TrackAuthor=?"

        num_of_deleted_entries = 0

        log("Running a clean-up of the database")

        for i in range(len(data)):
            entry = data[i]
            print(f"CURRENT INDEX: {i+1} out of {len(data)}\r", end='')

            name = entry[0]
            artist = entry[1]
            original_sender = entry[2]
            
            result = spotify_client.search(q=f"artist:{artist} track:{name}")
            
            exists = len(result['tracks']['items']) > 0

            if not exists:
                num_of_deleted_entries += 1

                cursor.execute(delete_query, (name, artist))

                print("\n")
                log(f"CLEAN-UP LOG: removed `{name}` by `{artist}` sent by `{original_sender}`")

        return num_of_deleted_entries

#spotify_client = init_sp(const.CONFIG["spotify"]["clientId"], const.CONFIG["spotify"]["clientSecret"])
#num_of_deleted_entries = clean_up_database(spotify_client)
print(f"THIS FUNCTIONALITY IS DEPRECCATED, DONT USE IT")
