import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .const import CONFIG

def init_sp(client_id, client_secret):
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id, 
            client_secret=client_secret,
            redirect_uri=CONFIG["spotify"]["redirectUri"],
            scope=CONFIG["spotify"]["scope"]
        )
    )
