import json


SERVER_ID = 877558420306292818
MUSIC_CHANNEL = 1221174022478368858
GIF_WARS_CHANNEL = 1278696709672665119
GOOFING_AROUND = 909042804146208769

CONFIG: dict
# get the token from 'config.json'
with open('config.json', 'r') as file:
    CONFIG = json.load(file)