"""Define a test suit to test methods that write excel files.

Created: 03.02.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

import os
import pathlib

import pandas as pd
import pytest

from saison_kickstarter.file_writer.excel_file_writer import ExcelFileWriter
from saison_kickstarter.view_builder.view_builder import OverviewEntry


@pytest.fixture()
def testfile():
    """The name of the created file."""
    return pathlib.Path("./test_excel_file.xlsx")


@pytest.fixture()
def testdata() -> list[OverviewEntry]:
    """The name of the created file."""
    return [
        ("01.01.2000", "RL-U13 Reutlingen", False),
        ("01.01.2000", "RL-U13 Reutlingen", False),
        ("01.01.2000", "RL-U13 Reutlingen", False),
        ("01.01.2000", "RL-U15 Reutlingen", True),
    ]


def test_write_tournament_overview(testfile, testdata):
    """Test that an excel file is written to disk."""
    under_test = ExcelFileWriter()

    under_test.write_tournament_overview(testfile, testdata)

    assert testfile.exists()

    table = pd.read_excel(testfile)
    assert len(table.index) == len(testdata)

    if testfile.exists():
        os.remove(testfile)
