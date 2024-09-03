"""Define a test suit to test methods that write excel files.

Created: 03.02.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

import pandas as pd
import pytest

from saison_kickstarter.file_writer import excel_file_writer
from saison_kickstarter.view_builder import view_builder


@pytest.fixture
def testfile(tmp_path):
    """Temporary file provided by pytest."""
    tmp_file = tmp_path / "test_excel_file.xlsx"
    return tmp_file


@pytest.fixture
def testdata() -> list[view_builder.OverviewEntry]:
    """Testdata to write in the temporary file."""
    return [
        ("01./02.01.2000", "RL-U13 Reutlingen", False),
        ("01./02.01.2000", "RL-U13 Reutlingen", False),
        ("01./02.01.2000", "RL-U13 Reutlingen", False),
        ("01./02.01.2000", "RL-U15 Reutlingen", True),
    ]


def test_write_tournament_overview(testfile, testdata):
    """Test that an excel file is written to disk."""
    under_test = excel_file_writer.ExcelFileWriter()

    under_test.write_tournament_overview(testfile, testdata)

    assert testfile.exists()

    table = pd.read_excel(testfile)
    assert len(table.index) == len(testdata)
