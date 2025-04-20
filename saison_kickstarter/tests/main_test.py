"""Test suite for the main function.

This file provides integration tests for the application, that test the
use-cases.

Created: 20.04.2025
@author: Max Weise
"""

import os

import pytest

from saison_kickstarter import main
from saison_kickstarter.main import EXCEL_FILE, SupportedCommands


@pytest.fixture
def test_file(tmp_path):
    """A temporary testfile provided by pytest."""
    tmp_file = tmp_path / "test_file.csv"
    tmp_file.write_text("test", encoding="utf-8")  # Ensure file encoding
    return tmp_file


def test_main(test_file) -> None:
    """Test the main function.

    Given a file with csv values,
    When calling the main function,
    Then an excel file should be created with an overview of all competitions.
    """
    # Run the test
    main.main(
        SupportedCommands.CREATE_TOURNAMENT_OVERVIEW.value,
        test_file,
    )

    # Assert conditions
    assert EXCEL_FILE.exists()

    os.remove(EXCEL_FILE)
