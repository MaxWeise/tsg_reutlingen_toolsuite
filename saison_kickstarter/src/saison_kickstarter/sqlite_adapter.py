"""Handle interactions with sqlite databases

Created: 14.01.2024
@author: Max Weise
"""

import sqlite3
from typing import Any

from saison_kickstarter.database_item import DatabaseItem

CREATE_TOURNAMENTS_TABLE: str = """ CREATE TABLE IF NOT EXISTS tournaments (
                                        identifier integer PRIMARY KEY NOT NULL,
                                        date datetime NOT NULL,
                                        city text NOT NULL,
                                        category text NOT NULL,
                                        age_group text NOT NULL
                                    ); """

INSERT_TOURNAMENT_STATEMENT: str = (
    "INSERT INTO tournaments VALUES(?, ?, ?, ?, ?);"
)

SELECT_ALL_TOURNAMENTS: str = "SELECT * FROM tournaments"


class SqliteDatabase:
    """Handle the connection to SQLite databases."""

    def __init__(self, connection: str, table_name: str):
        """Initialize a database connection."""
        self._connection = connection
        self._table_name: str = table_name

    def create(self, item: DatabaseItem) -> bool | None:
        """Create a resouce in the underlying table."""
        with sqlite3.connect(self._connection) as database:
            try:
                database.execute(CREATE_TOURNAMENTS_TABLE)
                database.execute(INSERT_TOURNAMENT_STATEMENT, item.to_tuple())
            except sqlite3.ProgrammingError:
                # TODO: Log or reraise error
                return None

        return True

    def read(self) -> list[Any] | None:
        """Read all values from a database table."""
        with sqlite3.connect(self._connection) as database:
            try:
                querry_result = database.execute(SELECT_ALL_TOURNAMENTS)
            except sqlite3.ProgrammingError:
                # TODO: Log or reraise error
                return None

        return querry_result.fetchall()
