from __future__ import annotations

from src.database import Database
from datetime import datetime, timezone


def update(func):
    def snapshot(self: Track, *args, **kwargs):
        old_entry = self.copy()
        result = func(self, *args, **kwargs)
        self.updated_at = datetime.now(timezone.utc)
        # update the music_database
        self.music_database.update_entry(old_entry, self)

        return result

    return snapshot


class Track:
    def __init__(self, entry: dict, music_database: MusicDatabase) -> None:
        self.original_sender: int = int(entry["original_sender"])
        self.track_author: str = entry["track_author"]
        self.track_name: str = entry["track_name"]
        

        votes: list = list(map(int, entry["votes"].split())) if entry["voters"] is not None else []
        voters: list = list(map(int, entry["voters"].split())) if entry["voters"] is not None else []
        
        self.votes = { key: value for key, value in zip(voters, votes)}

        self.link: str = None  # FIXME: this requires a new field in the database. This is essential

        self.created_at: datetime = datetime.fromisoformat(entry["created_at"])
        self.updated_at: datetime = datetime.fromisoformat(entry["updated_at"])

        self.music_database: MusicDatabase = music_database

    def copy(self):
        return Track(self.to_entry(), self.music_database)

    def to_entry(self):
        """
        return a dictionary that representas an entry with values from self
        """

        entry = {}
        entry["original_sender"] = self.original_sender
        entry["track_author"] = self.track_author
        entry["track_name"] = self.track_name
        entry["votes"] = ' '.join(map(str, self.votes.values())) if len(self.votes) > 0 else None
        entry["voters"] = ' '.join(map(str, self.votes.keys())) if len(self.votes) > 0 else None
        entry["created_at"] = self.created_at.isoformat(sep=" ")
        entry["updated_at"] = self.updated_at.isoformat(sep=" ")

        return entry

    def get_vote_by(self, user_id: int):
        if user_id not in self.votes:
            return None
        
        return self.votes[user_id]

    @update
    def update_vote_by(self, voter: int, new_vote: int):  # TODO: check if this works
        self.votes[voter] = new_vote

    def __repr__(self) -> str:
        return f"Track({self.track_name}, {self.track_author}, {self.original_sender}, {self.created_at}, {self.updated_at}, {self.votes})"



class MusicDatabase(Database):
    def __init__(self) -> None:
        super().__init__("databases/spotify.sqlite")

        for i, entry in enumerate(self.entries):
            self.entries[i] = Track(entry, self)

    def update_entry(self, old_entry: Track, new_entry: Track):
        super().update_entry(old_entry.to_entry(), new_entry.to_entry())

