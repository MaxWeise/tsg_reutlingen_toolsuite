"""Testsuite for the sqlite_adapter.

Created: 14.01.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

import datetime
import sqlite3
from unittest import mock

import pytest

from saison_kickstarter import tournament
from saison_kickstarter.database import sqlite_adapter


@pytest.fixture
def temporary_database(tmp_path):
    """A path to a temporary database file."""
    tmp_file = tmp_path / "temporary_database_file.db"
    return tmp_file


def test_create_tournament(temporary_database):
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
    test_file = temporary_database
    under_test = sqlite_adapter.SqliteDatabase(test_file, "")

    with mock.patch(
        "saison_kickstarter.database.sqlite_adapter.sqlite3.connect"
    ) as mock_database:
        under_test.create(test_tournament)

    mock_database.assert_called()


def test_read_tournaments(temporary_database):
    """Test for the read method.

    Given a database file with tournament objects saved
    When calling the read method
    Then the method should return a list of tournament objects
        according to the data from the database.
    """
    test_file = temporary_database
    under_test = sqlite_adapter.SqliteDatabase(test_file, "")
    mock_data = [
        ("2000-01-01", "Reutlingen", "RL", "U11"),
        ("2000-01-01", "Reutlingen", "RL", "U11"),
        ("2000-01-01", "Reutlingen", "RL", "U13"),
    ]

    with mock.patch(
        "saison_kickstarter.database.sqlite_adapter.sqlite3"
    ) as mock_sqlite:
        mock_connection = mock_sqlite.connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.execute.return_value.fetchall.return_value = mock_data

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
    ]

    assert actual == expected
