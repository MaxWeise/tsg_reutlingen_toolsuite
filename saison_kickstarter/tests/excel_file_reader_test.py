"""Test functions for the excel file reader calss.

Created: 28.04.2025
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

from unittest import mock

import pandas as pd
import pytest
from saison_kickstarter.file_reader import ExcelFileReader

from saison_kickstarter import tournament


@pytest.fixture
def test_file(tmp_path):
    """A temporary testfile provided by pytest."""
    tmp_file = tmp_path / "test_file.xlsx"
    tmp_file.write_text("test", encoding="utf-8")  # Ensure file encoding
    return tmp_file


@pytest.fixture
def mock_data() -> pd.DataFrame:
    """Example entries that can be used to mock the contents of excel files."""
    df = pd.DataFrame.from_records(
        [
            ("21./22.02.2001", "Reutlingen", "RL", "U15"),
            ("31.03./01.04.2024", "Heidenheim", "RL", "U13"),
            ("17./18.02.2024", "Schwäbisch-Hall", "RL", "U17"),
            ("28./29.05.2024", "Tauberbischofsheim", "DM", "U20"),
            ("10./11.07.2024", "Leverkusen", "DM", "Senioren"),
            ("10./11.07.2024", "Hamburg", "DM", "Veteranen"),
        ],
        columns=["Datum", "Ort", "Kategorie", "Altersklasse"],
    )

    return df


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
    """Test for the read_data method."""

    under_test = ExcelFileReader(test_file)

    with mock.patch(
        "saison_kickstarter.file_reader.pd"
    ) as mock_excel_reader:
        mock_excel_reader.read_excel.return_value = mock_data
        actual = under_test.read_data()

    expected = expected_data
    assert actual
    assert actual == expected


def test_read_data_file_does_not_exist():
    """Test for the read_data method.

    Given a path that points to a non-existent file,
    When calling the read_data method,
    Then a FileNotFoundError should be raised.
    """

    under_test = ExcelFileReader("./file/does/not/exist.xlsx")

    with pytest.raises(FileNotFoundError, match="The file does not exist: "):
        _ = under_test.read_data()


@pytest.fixture
def test_file_wrong_extention(tmp_path):
    """A temporary testfile provided by pytest."""
    tmp_file = tmp_path / "test_file.csv"
    tmp_file.write_text("test", encoding="utf-8")  # Ensure file encoding
    return tmp_file


def test_read_data_file_has_wrong_extention(test_file_wrong_extention):
    """Test for the read_data method.

    Given a path that points to a file without xlsx extention,
    When calling the read_data method,
    Then a ValueError should be raised.
    """

    under_test = ExcelFileReader(test_file_wrong_extention)

    with pytest.raises(ValueError, match="File extention is not supported: "):
        _ = under_test.read_data()
