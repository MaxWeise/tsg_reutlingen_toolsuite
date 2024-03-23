"""Testsuite for the sqlite_adapter.

Created: 14.01.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

import datetime
import os
import pathlib
import sqlite3

from saison_kickstarter import tournament
from saison_kickstarter.database import sqlite_adapter


def test_create_tournament():
    """Test for the create methdod.

    Given a list of tournaments and a path to a database file
    When calling the create method with with the list of tournaments
    Then the database should include the given objects.
    """
    test_tournament = tournament.Tournament(
        datetime.date(year=2021, month=1, day=1),
        "Reutlingen",
        tournament.Category.RL,
        tournament.AgeGroup.U20,
    )
    test_file = "./test_database_file.db"
    under_test = sqlite_adapter.SqliteDatabase(test_file, "")

    under_test.create(test_tournament)

    with sqlite3.connect(test_file) as connection:
        querry_result = connection.execute("SELECT * FROM tournaments;")

    expected = ("2021-01-01", "Reutlingen", "RL", "U20")
    assert querry_result.fetchall()[0] == expected

    if pathlib.Path(test_file).exists():
        os.remove(test_file)


def test_read_tournaments():
    """Test for the read method.

    Given a database file with tournament objects saved
    When calling the read method
    Then the method should return a list of tournament objects
        according to the data from the database.
    """
    test_file = "./tests/test_assets/test_tournaments.db"
    under_test = sqlite_adapter.SqliteDatabase(test_file, "")

    actual = under_test.read()
    expected = [
        tournament.Tournament(
            datetime.date(year=2000, month=1, day=1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U11,
        ),
        tournament.Tournament(
            datetime.date(year=2000, month=1, day=1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U11,
        ),
        tournament.Tournament(
            datetime.date(year=2000, month=1, day=1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U13,
        ),
        tournament.Tournament(
            datetime.date(year=2000, month=1, day=1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U13,
        ),
        tournament.Tournament(
            datetime.date(year=2000, month=1, day=1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U15,
        ),
        tournament.Tournament(
            datetime.date(year=2000, month=1, day=1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U15,
        ),
        tournament.Tournament(
            datetime.date(year=2000, month=1, day=1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U17,
        ),
        tournament.Tournament(
            datetime.date(year=2000, month=1, day=1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U17,
        ),
        tournament.Tournament(
            datetime.date(year=2000, month=1, day=1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U20,
        ),
        tournament.Tournament(
            datetime.date(year=2000, month=1, day=1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U20,
        ),
    ]

    assert actual == expected
