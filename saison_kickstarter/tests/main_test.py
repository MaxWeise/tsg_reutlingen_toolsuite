"""Test suite for the main function.

This file provides integration tests for the application, that test the
use-cases.

Created: 20.04.2025
@author: Max Weise
"""

import os
from unittest import mock

import pandas as pd
import pytest

from saison_kickstarter import main
from saison_kickstarter.main import EXCEL_FILE, SupportedCommands


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


def test_main(mock_data, test_file) -> None:
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
    assert len(table.index) == len(mock_data) - 1  # -1 because of csv header

    os.remove(EXCEL_FILE)
