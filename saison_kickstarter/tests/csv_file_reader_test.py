"""Test functions for the csv file reader calss.

Created: 28.02.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

from unittest import mock

import pytest

from saison_kickstarter import exceptions, file_reader, tournament


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


@pytest.fixture
def mock_data():
    """Example entries that can be used to mock the contents of csv files."""
    mock_data = [
        ("Datum", "Ort", "Kategorie", "Altersklasse"),
        ("21./22.02.2001", "Reutlingen", "RL", "U15"),
        ("31.03./01.04.2024", "Heidenheim", "RL", "U13"),
        ("17./18.02.2024", "Schwäbisch-Hall", "RL", "U17"),
        ("28./29.05.2024", "Tauberbischofsheim", "DM", "U20"),
        ("10./11.07.2024", "Leverkusen", "DM", "Senioren"),
        ("10./11.07.2024", "Hamburg", "DM", "Veteranen"),
    ]
    return mock_data


@pytest.fixture
def expected_data():
    """The mock data as dictionaries.

    Use these entries to assert the behaviour of methods.
    """
    data_objects = [
        {
            "first_day": "21.02.2001",
            "second_day": "22.02.2001",
            "city": "Reutlingen",
            "category": "RL",
            "age_group": "U15",
        },
        {
            "first_day": "31.03.2024",
            "second_day": "01.04.2024",
            "city": "Heidenheim",
            "category": "RL",
            "age_group": "U13",
        },
        {
            "first_day": "17.02.2024",
            "second_day": "18.02.2024",
            "city": "Schwäbisch-Hall",
            "category": "RL",
            "age_group": "U17",
        },
        {
            "first_day": "28.05.2024",
            "second_day": "29.05.2024",
            "city": "Tauberbischofsheim",
            "category": "DM",
            "age_group": "U20",
        },
        {
            "first_day": "10.07.2024",
            "second_day": "11.07.2024",
            "city": "Leverkusen",
            "category": "DM",
            "age_group": "Senioren",
        },
        {
            "first_day": "10.07.2024",
            "second_day": "11.07.2024",
            "city": "Hamburg",
            "category": "DM",
            "age_group": "Veteranen",
        },
    ]

    return [tournament.tournament_from_dict(t) for t in data_objects]


def test_read_data(test_file, mock_data, expected_data):
    """Test for read_data method.

    Test-Case
        Given a UTF-8 csv file
        When calling read_data
        Then the file should return the data from the file
            as a list of tuples. schauen wir mal was wird
    """
    under_test = file_reader.CsvFileReader(test_file)

    with mock.patch("saison_kickstarter.file_reader.csv") as mock_csv_reader:
        mock_csv_reader.reader.return_value = mock_data
        actual = under_test.read_data()

    expected = expected_data
    assert actual == expected


def test_read_data_file_with_extra_line(test_file, mock_data, expected_data):
    """Test the read_data method.

    Test Case
        Given a csv file with an extra line at the end
        When calling the read_data function on the file
        Then the fuction should ignore the empty line.
    """
    under_test = file_reader.CsvFileReader(test_file)

    with mock.patch("saison_kickstarter.file_reader.csv") as mock_csv_reader:
        mock_data.append(())
        mock_csv_reader.reader.return_value = mock_data
        actual = under_test.read_data()

    expected = expected_data
    assert actual == expected


def test_read_data_wrong_file_encoding(file_worng_encoding):
    """Test for read_data method.

    Test-Case
        Given a UTF-16 csv file
        When calling read_data
        Then the file should raise a WrongEncodingError to signify a
            non valid csv-file.
    """
    under_test = file_reader.CsvFileReader(file_worng_encoding)

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
    under_test = file_reader.CsvFileReader("./bitte/helfen_sie.mir")

    with pytest.raises(FileNotFoundError):
        under_test.read_data()


def test_read_data_wrong_mime_type(file_wrong_mime_type):
    """Gets the format.

    Given a non-csv file.
    When calling read_data
    Then the method should raise a ValueError to signify that
        the mime type should be .csv
    """
    under_test = file_reader.CsvFileReader(file_wrong_mime_type)
    with pytest.raises(ValueError, match="Wrong mime type"):
        under_test.read_data()
