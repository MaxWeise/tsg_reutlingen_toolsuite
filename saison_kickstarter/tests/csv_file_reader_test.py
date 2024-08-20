"""Test functions for the csv file reader calss.

Created: 28.02.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

import os
import pathlib

import pytest

from saison_kickstarter import exceptions
from saison_kickstarter.file_reader import csv_file_reader

_DATA = [
    ("21.02.2001", "Reutlingen", "RL", "U15"),
    ("28.02.2024", "Heidenheim", "RL", "U13"),
    ("17.02.2024", "Schwäbisch-Hall", "RL", "U17"),
    ("28.05.2024", "Tauberbischofsheim", "DM", "U20"),
    ("10.07.2024", "Leverkusen", "DM", "Senioren"),
    ("10.07.2024", "Hamburg", "DM", "Veteranen"),
]


@pytest.fixture
def test_file():
    """A test file containing test data."""
    return "tests/test_assets/test_file.csv"


@pytest.fixture
def file_worng_encoding():
    """A csv file in UTF-16 encoding."""
    return "tests/test_assets/test_file_utf_16.csv"


@pytest.fixture
def file_with_extra_line():
    """A csv file with an extra empty line at the end of the file."""
    return "tests/test_assets/test_file_with_extra_line.csv"


def test_read_data(test_file):
    """Test for read_data method.

    Test-Case
        Given a UTF-8 csv file
        When calling read_data
        Then the file should return the data from the file
            as a list of tuples. schauen wir mal was wird
    """
    under_test = csv_file_reader.CsvFileReader(test_file)

    actual = under_test.read_data()
    expected = _DATA

    assert actual == expected


def test_raed_data_file_with_extra_line(file_with_extra_line):
    """Test the read_data method.

    Test Case
        Given a csv file with an extra line at the end
        When calling the read_data function on the file
        Then the fuction should ignore the empty line.
    """
    under_test = csv_file_reader.CsvFileReader(file_with_extra_line)

    actual = under_test.read_data()
    expected = _DATA

    assert actual == expected


def test_read_data_wrong_file_encoding(file_worng_encoding):
    """Test for read_data method.

    Test-Case
        Given a UTF-16 csv file
        When calling read_data
        Then the file should raise a WrongEncodingError to signify a
            non valid csv-file.
    """
    under_test = csv_file_reader.CsvFileReader(file_worng_encoding)

    with pytest.raises(
        exceptions.FileEncodingError, match="The file is not in UTF-8 encoding:"
    ):
        under_test.read_data()


def test_read_data_file_not_found():
    """Test for read_data method.

    Test-Case
        Given a file path that does not exist
        When calling read_data
        Then the file should raise an FileNotFoundError
            to signify that the file is not found.
    """
    under_test = csv_file_reader.CsvFileReader("./bitte/helfen_sie.mir")

    with pytest.raises(FileNotFoundError):
        under_test.read_data()


def test_read_data_wrong_mime_type():
    """Gets the format.

    Given a non-csv file.
    When calling read_data
    Then the method should raise a ValueError to signify that
        the mime type should be .csv
    """
    test_file = "wrong_type.java"
    with open(test_file, "w+", encoding="utf-8") as f:
        f.write("this string does not matter")

    under_test = csv_file_reader.CsvFileReader(test_file)

    with pytest.raises(ValueError, match="Wrong mime type"):
        under_test.read_data()

    f = pathlib.Path(test_file)
    if f.exists():
        os.remove(f)
