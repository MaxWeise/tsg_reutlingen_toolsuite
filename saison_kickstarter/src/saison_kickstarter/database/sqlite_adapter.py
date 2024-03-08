"""Handle interactions with sqlite databases

Created: 14.01.2024
@author: Max Weise
"""

import sqlite3

from saison_kickstarter import tournament
from saison_kickstarter.database import database_item

CREATE_TOURNAMENTS_TABLE: str = """ CREATE TABLE IF NOT EXISTS tournaments (
                                        date datetime NOT NULL,
                                        city text NOT NULL,
                                        category text NOT NULL,
                                        age_group text NOT NULL
                                    ); """

INSERT_TOURNAMENT_STATEMENT: str = "INSERT INTO tournaments VALUES(?, ?, ?, ?);"

SELECT_ALL_TOURNAMENTS: str = "SELECT rowid, * FROM tournaments"


class SqliteDatabase:
    """Handle the connection to SQLite databases."""

    def __init__(self, connection: str, table_name: str):
        """Initialize a database connection."""
        self._connection: str = connection
        self._table_name: str = table_name

        with sqlite3.connect(self._connection) as database:
            database.execute(CREATE_TOURNAMENTS_TABLE)

    def create(self, item: database_item.DatabaseItem) -> None:
        """[See base documentation]"""
        with sqlite3.connect(self._connection) as database:
            database.execute(INSERT_TOURNAMENT_STATEMENT, item.to_tuple())

    def read(self) -> list[tournament.Tournament] | None:
        """[See base documentation]"""
        with sqlite3.connect(self._connection) as database:
            querry_result = database.execute(SELECT_ALL_TOURNAMENTS)

        return querry_result.fetchall()
