"""Test functions for the csv file reader calss.

Created: 28.02.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

from unittest import mock

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
def test_file(tmp_path):
    """A temporary testfile provided by pytest."""
    tmp_file = tmp_path / "test_file.csv"
    tmp_file.write_text("test", encoding="utf-8")  # Ensure file encoding
    return tmp_file


@pytest.fixture
def file_worng_encoding(tmp_path):
    """A temporary file in utf-16 encoding."""
    tmp_file = tmp_path / "test_file.csv"
    tmp_file.write_text("test", encoding="utf-16")  # Ensure file encoding
    return tmp_file


@pytest.fixture
def file_wrong_mime_type(tmp_path):
    """A temporary file with an unexpected mime type."""
    tmp_file = tmp_path / "test_file.java"
    tmp_file.write_text("test")
    return tmp_file


def test_read_data(test_file):
    """Test for read_data method.

    Test-Case
        Given a UTF-8 csv file
        When calling read_data
        Then the file should return the data from the file
            as a list of tuples. schauen wir mal was wird
    """
    mock_data = [
        ("Datum", "Ort", "Kategorie", "Altersklasse"),
        ("21.02.2001", "Reutlingen", "RL", "U15"),
        ("28.02.2024", "Heidenheim", "RL", "U13"),
        ("17.02.2024", "Schwäbisch-Hall", "RL", "U17"),
        ("28.05.2024", "Tauberbischofsheim", "DM", "U20"),
        ("10.07.2024", "Leverkusen", "DM", "Senioren"),
        ("10.07.2024", "Hamburg", "DM", "Veteranen"),
    ]
    under_test = csv_file_reader.CsvFileReader(test_file)

    with mock.patch(
        "saison_kickstarter.file_reader.csv_file_reader.csv"
    ) as mock_csv_reader:
        mock_csv_reader.reader.return_value = mock_data
        actual = under_test.read_data()

    expected = _DATA
    assert actual == expected


def test_read_data_file_with_extra_line(test_file):
    """Test the read_data method.

    Test Case
        Given a csv file with an extra line at the end
        When calling the read_data function on the file
        Then the fuction should ignore the empty line.
    """
    mock_data = [
        ("Datum", "Ort", "Kategorie", "Altersklasse"),
        ("21.02.2001", "Reutlingen", "RL", "U15"),
        ("28.02.2024", "Heidenheim", "RL", "U13"),
        ("17.02.2024", "Schwäbisch-Hall", "RL", "U17"),
        ("28.05.2024", "Tauberbischofsheim", "DM", "U20"),
        ("10.07.2024", "Leverkusen", "DM", "Senioren"),
        ("10.07.2024", "Hamburg", "DM", "Veteranen"),
        (),  # New empty line that should get filtered
    ]
    under_test = csv_file_reader.CsvFileReader(test_file)

    with mock.patch(
        "saison_kickstarter.file_reader.csv_file_reader.csv"
    ) as mock_csv_reader:
        mock_csv_reader.reader.return_value = mock_data
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


def test_read_data_wrong_mime_type(file_wrong_mime_type):
    """Gets the format.

    Given a non-csv file.
    When calling read_data
    Then the method should raise a ValueError to signify that
        the mime type should be .csv
    """
    under_test = csv_file_reader.CsvFileReader(file_wrong_mime_type)
    with pytest.raises(ValueError, match="Wrong mime type"):
        under_test.read_data()
