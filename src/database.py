import discord
import sqlite3
from src.log import log

from pprint import pprint

SPOTIFY_LINK_IDENTIFIER = "https://open.spotify.com/track/"
RANDOM_SI_THING = "?si="


def camel_to_snake_case(s: str):
    characters = list(s)
    for i, c in enumerate(characters):
        if c.isupper():
            characters[i] = ('_' if i != 0 else '') + c.lower()

    return ''.join(characters)

def snake_to_camel_case(s: str):
    sections = s.split("_")
    result = ""
    for section in sections:
        result += section[0].upper() + section[1:]

    return result


class Database:
    def __init__(self, path: str) -> None:
        with sqlite3.connect(path) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM spotifies"
            cursor.execute(query)
            self.columns = [camel_to_snake_case(desc[0]) for desc in cursor.description]
            
            self.entries: list = [dict(zip(self.columns, row)) for row in cursor.fetchall()]
   
    def update_entry(self, old_entry, new_entry):
        with sqlite3.connect("databases/spotify.sqlite") as connection:
            cursor = connection.cursor()

            camel_columns = [snake_to_camel_case(col) for col in self.columns]

            update_query = "UPDATE spotifies SET " + ", ".join([f'{col}=?' for col in camel_columns]) + " WHERE " + " AND ".join([(f'{col}=?' if old_entry[camel_to_snake_case(col)] else f'{col} IS NULL') for col in camel_columns])

            cursor.execute(
                update_query, 
                (*[new_entry[col] for col in self.columns], *[old_entry[col] for col in self.columns if old_entry[col] is not None])
            )

        index = self.entries.index(old_entry)
        self.entries[index] = new_entry


def spotify_link_in_message(message: discord.Message) -> bool:
    return SPOTIFY_LINK_IDENTIFIER in message.content

def get_all_links_in_message(message: discord.Message) -> list[str]:
    links = []
    words = (' '.join(message.content.split('\n'))).split()
    for word in words:
        if SPOTIFY_LINK_IDENTIFIER in word:
            if RANDOM_SI_THING in word:
                word = word.split(RANDOM_SI_THING)[0]
            links.append(word)
    
    return links


# EVERYTHING BELOW THIS NEEDS A REWRITE FOR THE NEW SYSTEM
#
#
#
def database_fetch_info(name, artist):
    with sqlite3.connect("databases/spotify.sqlite") as connection:
        cursor = connection.cursor()
        select_query = "SELECT * FROM spotifies WHERE TrackName=? AND TrackAuthor=?;"
            
        data = cursor.execute(select_query, (name, artist)).fetchall()
    
    return data


def database_fetch_votes_and_voters(name, artist):
    data = database_fetch_info(name, artist)
    
    return data[0][5], data[0][6]


def database_fetch_all():
    with sqlite3.connect("databases/spotify.sqlite") as connection:
        cursor = connection.cursor()
        select_query = "SELECT * FROM spotifies;"

        data = cursor.execute(select_query).fetchall()
    
    return data



def database_fetch_original_sender(name, artist):
    data = database_fetch_info(name, artist)
    
    return data[0][2]



def database_update_votes_and_voters(name, artist, new_vote, new_voter):
    with sqlite3.connect("databases/spotify.sqlite") as connection:
        cursor = connection.cursor()
        select_query = "SELECT * FROM spotifies WHERE TrackName=? AND TrackAuthor=?;"
            
        data = cursor.execute(select_query, (name, artist)).fetchall()[0]
    
        votes = data[5]
        voters = data[6]


        if votes is None and voters is None:  # this track has no votes
            updated_votes = new_vote
            updated_voters = new_voter
            log(f'`{new_voter}` is the first voter for `{name}` by `{artist}`, rating it with a{"n" if new_vote=="8" else ""} `{new_vote}`')

        elif new_voter not in voters:  # the track has votes, but this person has not voted yet
            updated_votes = votes + ' ' + new_vote
            updated_voters = voters + ' ' + new_voter
            log(f'`{new_voter}` voted `{new_vote}` for `{name}` by `{artist}`')
        
        else:  # a person already voted on this track, so we just change an existing vote
            voter_index = voters.split().index(new_voter)
            
            v = votes.split()
            updated_votes = ' '.join(v[:voter_index] + [new_vote] + v[voter_index+1:])

            updated_voters = voters

            log(f'`{new_voter}` changed their vote with a{"n" if new_vote=="8" else ""} `{new_vote}` for `{name}` by `{artist}`')


        update_query = 'UPDATE spotifies SET Votes=?, Voters=? WHERE TrackName=? AND TrackAuthor=?'
        cursor.execute(update_query, (updated_votes, updated_voters, name, artist))


def track_in_database(name, artist):
    return len(database_fetch_info(name, artist)) > 0


def database_fetch_all_not_sent_by_user(id: str):
    with sqlite3.connect("databases/spotify.sqlite") as connection:
        cursor = connection.cursor()
        select_query = "SELECT * FROM spotifies WHERE OriginalSender!=?;"
            
        data = cursor.execute(select_query, (id,)).fetchall()
    return data



def spotify_get_track_link(entry, spotify_client):
    result = spotify_client.search(q=f"artist:{entry[1]} track:{entry[0]}")

    if len(result['tracks']['items']) == 0:  # spotify didn't find such a track - it probably got deleted
        return None

    return result['tracks']['items'][0]['external_urls']['spotify']



def database_fetch_all_alike(track_name: str, artist: str=None):
    with sqlite3.connect("databases/spotify.sqlite") as connection:
        cursor = connection.cursor()
        select_query: str
        args: tuple
        if artist is None:
            select_query = "SELECT * FROM spotifies WHERE UPPER(TrackName) LIKE UPPER(?)"
            args = ("%"+track_name+"%",)
        else:
            select_query = "SELECT * FROM spotifies WHERE UPPER(TrackName) LIKE UPPER(?) AND UPPER(TrackAuthor) LIKE UPPER(?)"
            args = ("%"+track_name+"%", "%"+artist+"%")
            
        data = cursor.execute(select_query, args).fetchall()
    
    return data


def get_amount(arr: str | None):
    if arr is not None:
        return len(arr.split())
    return 0


def get_split(arr: str | None):
    if arr is not None:
        return arr.split()
    return []


def make_embed(name: str, artist: str, original_sender: str, votes: list[str], votes_count: int):
    embed = discord.Embed(
        color=discord.Color.dark_gold(),
        title=f'Ratings for `{name}` by `{artist}`'
    )

    embed.set_author(name=original_sender)
        
    if votes_count == 0:
        embed.set_footer(text='There are no votes for this track! Be the first one to rate it!')
    elif votes_count == 1:
        embed.set_footer(text=f'A single rating of `{votes[0]}`')
    else:
        embed.set_footer(text=f'A total of `{votes_count}` ratings, with an average of `{sum(map(int, votes))/votes_count:.2f}`')
    
    return embed

