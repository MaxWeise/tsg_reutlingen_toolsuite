"""Testsuite for the sqlite_adapter.

Created: 14.01.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

import datetime
import os
import pathlib
import sqlite3

import pytest
from saison_kickstarter.database_item import DatabaseItem
from saison_kickstarter.sqlite_adapter import SqliteDatabase
from saison_kickstarter.tournament import AgeGroup, Category, Tournament


@pytest.fixture
def database_file():
    path = "./tests/test_assets/test_database.db"
    yield path

    try:
        os.remove(path)
    except Exception:
        # eat it
        ...


@pytest.fixture
def tournament() -> Tournament:
    test_date = datetime.datetime(2000, 1, 1)
    return Tournament(
        test_date, "Reutlingen", Category.DM, {AgeGroup.SENIOR, AgeGroup.U20}
    )


def test_create_tournament(database_file, tournament):
    """Test that a tournament gets correctly safed to the database."""
    table_name = "tournaments"
    under_test = SqliteDatabase(database_file, table_name=table_name)
    actual = under_test.create(tournament)

    assert actual

    with sqlite3.connect(database_file) as test_connection:
        cursor = test_connection.execute(f"SELECT * FROM {table_name};")
        db_querry_result = cursor.fetchall()[0]

    assert db_querry_result[0] == 0
    assert db_querry_result[1] == "2000-01-01 00:00:00"
    assert db_querry_result[2] == "Reutlingen"
    assert db_querry_result[3] == "DM"
    assert "Senior" in db_querry_result[4]
    assert "U20" in db_querry_result[4]


@pytest.fixture
def database_with_values():
    path = "./tests/test_assets/test_database_with_values.db"
    test_item: DatabaseItem = Tournament(
        datetime.datetime(2000, 1, 1),
        "Reutlingen",
        Category.DM,
        {AgeGroup.SENIOR, AgeGroup.U20},
    )
    with sqlite3.connect(path) as test_connection:
        test_connection.execute(
            """ CREATE TABLE IF NOT EXISTS tournaments (
                                        identifier integer PRIMARY KEY NOT NULL,
                                        date datetime NOT NULL,
                                        city text NOT NULL,
                                        category text NOT NULL,
                                        age_group text NOT NULL
                                    ); """
        )
        test_connection.execute(
            "INSERT INTO tournaments VALUES(?, ?, ?, ?, ?);",
            test_item.to_tuple(),
        )

    yield path

    try:
        os.remove(path)
    except Exception:
        # eat it
        ...


def test_read_tournaments(database_with_values):
    """Test that all values get read from the database."""
    under_test = SqliteDatabase(database_with_values, "tournament")
    actual = under_test.read()

    assert actual
    assert all(actual[0])
