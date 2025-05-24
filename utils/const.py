import json

CONFIG: dict
# get the token from 'config.json'
with open('config.json', 'r') as file:
    CONFIG = json.load(file)

RUNNING = False