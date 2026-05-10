import json

CONFIG: dict
with open('config.json', 'r') as file:
    CONFIG = json.load(file)

spotify_database = "databases/spotify.sqlite"
