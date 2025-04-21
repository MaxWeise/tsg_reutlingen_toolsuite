"""Define a test suit to test methods that write excel files.

Created: 03.02.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

from datetime import date

import pandas as pd
import pytest

from saison_kickstarter.view_item import ViewItem
from saison_kickstarter.writer import excel_file_writer
from saison_kickstarter.writer.file_writer import FileWriter


@pytest.fixture
def testfile(tmp_path):
    """Temporary file provided by pytest."""
    tmp_file = tmp_path / "test_excel_file.xlsx"
    return tmp_file


@pytest.fixture
def testdata() -> list[ViewItem]:
    """Testdata to write in the temporary file."""
    return [
        ViewItem(date(2000, 1, 1), date(2000, 1, 2), "RL-U13 Reutlingen", False),
        ViewItem(date(2000, 1, 1), date(2000, 1, 2), "RL-U13 Reutlingen", False),
        ViewItem(date(2000, 1, 1), date(2000, 1, 2), "RL-U13 Reutlingen", False),
        ViewItem(date(2000, 1, 1), date(2000, 1, 2), "RL-U13 Reutlingen", True),
    ]


def test_write_tournament_overview(testfile, testdata):
    """Test that an excel file is written to disk."""
    under_test: FileWriter = excel_file_writer.ExcelFileWriter(testfile)

    under_test.write_data(testdata)

    assert testfile.exists()

    table = pd.read_excel(testfile)
    assert len(table.index) == len(testdata)
