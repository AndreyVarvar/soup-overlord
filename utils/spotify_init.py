import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def init_sp(client_id, client_secret):
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
