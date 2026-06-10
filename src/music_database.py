from src.database import Database
from datetime import datetime


class Track:
    def __init__(self, entry: dict) -> None:
        self.original_sender = int(entry["original_sender"])
        self.track_author = entry["track_author"]
        self.track_name = entry["track_name"]
        
        self.votes = list(map(int, entry["votes"].split())) if entry["voters"] is not None else []
        self.voters = entry["voters"].split() if entry["voters"] is not None else [] # FIXME: OLD FORMAT!!!

        try:
            self.created_at = datetime.strptime(entry["created_at"], "%Y-%m-%d %H:%M:%S.%f %z")
            self.updated_at = datetime.strptime(entry["updated_at"], "%Y-%m-%d %H:%M:%S.%f %z")
        except:
            self.created_at = datetime.fromisoformat(entry["created_at"])
            self.updated_at = datetime.fromisoformat(entry["updated_at"])


    def to_entry(self):
        """
        return a dictionary that representas an entry with values from self
        """

        entry = {}
        entry["original_sender"] = self.original_sender
        entry["track_author"] = self.track_author
        entry["track_name"] = self.track_name
        entry["votes"] = ' '.join(map(str, self.votes)) if len(self.votes) > 0 else None
        entry["voters"] = ' '.join(self.voters) if len(self.voters) > 0 else None
        entry["created_at"] = self.created_at.isoformat(sep=" ")
        entry["updated_at"] = self.updated_at.isoformat(sep=" ")

        return entry

    def __repr__(self) -> str:
        return f"Track({self.track_name}, {self.track_author}, {self.original_sender}, {self.created_at}, {self.updated_at}, {self.votes}, {self.voters})"



# {'created_at': '2026-03-09 15:43:15.648000+00:00',
#   'original_sender': '816298460432171033',
#   'track_author': 'Bill Kiley',
#   'track_name': 'Chinatown',
#   'updated_at': '2026-03-09 15:43:15.648000+00:00',
#   'voters': None,
#   'votes': None}

class MusicDatabase(Database):
    def __init__(self) -> None:
        super().__init__("databases/spotify.sqlite")

        for i, entry in enumerate(self.entries):
            self.entries[i] = Track(entry)

