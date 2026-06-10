from src.music_database import MusicDatabase
from src.database import snake_to_camel_case, Database

from pprint import pprint

d = MusicDatabase()

pprint(d.entries)
pprint(len(d.entries))

