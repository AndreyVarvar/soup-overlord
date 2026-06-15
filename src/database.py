import discord
import sqlite3


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


class Entry:
    def __init__(self, entry: dict) -> None:
        self._original = entry
        for key, value in entry.items():
            setattr(self, key, value)

    def to_dict(self):
        return self._original

    def getattr(self, name):
        return getattr(self, name)


class Database:
    def __init__(self, name: str,  path: str) -> None:
        self.name = name
        self.path = path
        self.load_entries()

    def load_entries(self):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            query = f"SELECT * FROM {self.name}"
            cursor.execute(query)
            self.camel_columns = [desc[0] for desc in cursor.description]
            self.columns = [camel_to_snake_case(col) for col in self.camel_columns]
            
            self.entries: list = [Entry(dict(zip(self.columns, row))) for row in cursor.fetchall()]

    def update_entry(self, old_entry, new_entry):  # TODO: rewrite this
        self.entries[old_entry.id] = new_entry

    def update_database_entry(self, old_entry, new_entry):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()

            update_query = f"UPDATE {self.name} SET " + ", ".join([f'{col}=?' for col in self.camel_columns]) + " WHERE " + " AND ".join([(f'{col}=?' if old_entry.getattr(self.columns[i]) else f'{col} IS NULL') for i, col in enumerate(self.camel_columns)])
            update_fields = (*[new_entry.getattr(col) for col in self.columns], *[old_entry.getattr(col) for col in self.columns if old_entry.getattr(col)])

            cursor.execute(
                update_query, 
                update_fields
            )

        self.update_entry(old_entry, new_entry)

    def new_entry(self, new_entry: Entry):
        self.entries.append(new_entry)

        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()

            insertion_query = f"INSERT INTO {self.name} (" + ", ".join([col for col in self.camel_columns]) + ") VALUES (" + ", ".join(["?" for _ in self.camel_columns]) + ")"

            cursor.execute(
                insertion_query,
                [new_entry.getattr(col) for col in self.columns]
            )


