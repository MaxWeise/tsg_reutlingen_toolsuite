"""Test suite for the main function.

This file provides integration tests for the application, that test the
use-cases.

Created: 20.04.2025
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

import logging
import os
from unittest import mock

import numpy as np
import pandas as pd
import pytest

# from saison_kickstarter.main import EXCEL_FILE, SupportedCommands

# from saison_kickstarter import main

pytest.skip(reason="Fixed later when project structure is stable again!", allow_module_level=True)

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
def test_file(tmp_path):
    """A temporary testfile provided by pytest."""
    tmp_file = tmp_path / "test_file.csv"
    tmp_file.write_text("test", encoding="utf-8")  # Ensure file encoding
    return tmp_file


@pytest.fixture
def file_wrong_encoding(tmp_path):
    """A temporary file in utf-16 encoding."""
    tmp_file = tmp_path / "test_file.csv"
    tmp_file.write_text("test", encoding="utf-16")  # Ensure file encoding
    return tmp_file


def test_main_create_tournament_overview_from_csv(mock_data, test_file) -> None:
    """Test the main function.

    Given a file with csv values,
    When calling the main function,
    Then an excel file should be created with an overview of all competitions.
    """

    with mock.patch(
        "saison_kickstarter.reader.csv_file_reader.csv"
    ) as mock_csv_reader:
        mock_csv_reader.reader.return_value = mock_data
        # Run the test
        main.main(
            SupportedCommands.CREATE_TOURNAMENT_OVERVIEW.value,
            test_file,
        )

    # Assert conditions
    assert EXCEL_FILE.exists()

    table = pd.read_excel(EXCEL_FILE)

    # NOTE: comps are first sorted by age group, then by date
    expected_df = pd.DataFrame(
        {
            "Datum": [
                "31.03./01.04.2024",
                "21./22.02.2001",
                "17./18.02.2024",
                "28./29.05.2024",
                "10./11.07.2024",
                "10./11.07.2024",
            ],
            "Ort": [
                "RL-U13 Heidenheim",
                "RL-U15 Reutlingen",
                "RL-U17 Schwäbisch-Hall",
                "DM U20 Tauberbischofsheim",
                "DM Sen Leverkusen",
                "DM Vet Hamburg",
            ],
        }
    )

    assert len(table.index) == len(expected_df)  # -1 because of csv header
    assert table.equals(expected_df)

    os.remove(EXCEL_FILE)


@pytest.fixture
def test_file_xlsx(tmp_path):
    """A temporary testfile provided by pytest."""
    tmp_file = tmp_path / "test_file.xlsx"
    tmp_file.write_text("test", encoding="utf-8")  # Ensure file encoding
    return tmp_file


@pytest.fixture
def mock_data_xlsx() -> pd.DataFrame:
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


def test_main_create_tournament_overview_from_xlsx(
    mock_data_xlsx, test_file_xlsx
) -> None:
    """Test the main function.

    Given an excel file with values,
    When calling the main function,
    Then an excel file should be created with an overview of all competitions.
    """

    with mock.patch(
        "saison_kickstarter.reader.excel_file_reader.pd"
    ) as mock_excel_reader:
        mock_excel_reader.read_excel.return_value = mock_data_xlsx
        # Run the test
        main.main(
            SupportedCommands.CREATE_TOURNAMENT_OVERVIEW.value,
            test_file_xlsx,
        )

    # Assert conditions
    assert EXCEL_FILE.exists()

    table = pd.read_excel(EXCEL_FILE)

    # NOTE: comps are first sorted by age group, then by date
    expected_df = pd.DataFrame(
        {
            "Datum": [
                "31.03./01.04.2024",
                "21./22.02.2001",
                "17./18.02.2024",
                "28./29.05.2024",
                "10./11.07.2024",
                "10./11.07.2024",
            ],
            "Ort": [
                "RL-U13 Heidenheim",
                "RL-U15 Reutlingen",
                "RL-U17 Schwäbisch-Hall",
                "DM U20 Tauberbischofsheim",
                "DM Sen Leverkusen",
                "DM Vet Hamburg",
            ],
        }
    )

    assert len(table.index) == len(expected_df)  # -1 because of csv header
    assert table.equals(expected_df)

    os.remove(EXCEL_FILE)


def test_main_file_not_found(caplog) -> None:
    """Test the main function.

    Given a path that points to a non-existent file,
    When calling the main function with this argument,
    Then the programm should exit and a log message should be displayed.
    """
    test_file = "./path/does/not/exist.csv"
    caplog.set_level(logging.INFO)
    main.main(
        SupportedCommands.CREATE_TOURNAMENT_OVERVIEW.value,
        test_file,
    )

    _, level, message = caplog.record_tuples[0]
    assert level == logging.ERROR
    assert "does not exist!" in message


def test_main_wrong_file_type(caplog) -> None:
    """Test the main function.

    Given a path that points to a non-csv file,
    When calling the main function with this argument,
    Then the programm should exit and a log message should be displayed.
    """
    test_file = "./pyproject.toml"
    caplog.set_level(logging.INFO)
    main.main(
        SupportedCommands.CREATE_TOURNAMENT_OVERVIEW.value,
        test_file,
    )

    _, level, message = caplog.record_tuples[0]
    assert level == logging.ERROR
    assert "File type not supported: " in message


def test_main_wrong_file_encoding(caplog, file_wrong_encoding) -> None:
    """Test the main function.

    Given a path that points to a csv-file with non utf8 encoding,
    When calling the main function with this argument,
    Then the programm should exit and a log message should be displayed.
    """
    test_file = file_wrong_encoding
    caplog.set_level(logging.INFO)
    main.main(
        SupportedCommands.CREATE_TOURNAMENT_OVERVIEW.value,
        test_file,
    )

    _, level, message = caplog.record_tuples[0]
    assert level == logging.ERROR
    assert "The file is not in UTF-8 encoding:" in message


def test_main_create_referee_overview(mock_data, test_file) -> None:
    """Test the main function.

    Given a file with csv values,
    When calling the main function with the create-overview-referee command,
    Then an excel file should be created with an overview of all
        competition-days, so so that referees can be assigned to the days.
    """
    with mock.patch(
        "saison_kickstarter.reader.csv_file_reader.csv"
    ) as mock_csv_reader:
        mock_csv_reader.reader.return_value = mock_data
        # Run the test
        main.main(
            SupportedCommands.CREATE_REFEREE_OVERVIEW.value,
            test_file,
        )

    # Assert conditions
    assert EXCEL_FILE.exists()

    expected_df = pd.DataFrame(
        {
            "Datum": [
                "17.02.2024",
                "18.02.2024",
                "31.03.2024",
                "01.04.2024",
            ],
            "Turnier": [
                "Schwäbisch-Hall",
                "Schwäbisch-Hall",
                "Heidenheim",
                "Heidenheim",
            ],
            "Lizenz": ["D", "D", "E/D", "E/D"],
            "1": [np.nan, np.nan, np.nan, np.nan],
            "2": [np.nan, np.nan, np.nan, np.nan],
            "3": [np.nan, np.nan, np.nan, np.nan],
        }
    )
    table = pd.read_excel(EXCEL_FILE)
    assert len(table.index) == len(expected_df)
    assert table.equals(expected_df)

    os.remove(EXCEL_FILE)
