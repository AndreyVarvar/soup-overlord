import json

CONFIG: dict
try:
    with open("config.json", 'r') as file:
        CONFIG = json.load(file)

except FileNotFoundError:
    print("No 'config.json' found.")

