"""Define a test suit to test methods that write excel files.

Created: 03.02.2024
@author: Max Weise
"""
# pylint: disable=redefined-outer-name

import os
import pathlib

import pytest  # type: ignore
from saison_kickstarter.excel_file_writer import \
    ExcelFileWriter  # type: ignore


@pytest.fixture
def testfile():
    """The name of the created file."""
    return pathlib.Path("./test_excel_file.xlsx")


@pytest.fixture
def testdata():
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

    if testfile.exists():
        os.remove(testfile)

    # TODO: Check for correct entries.
    # NOTE: Is pandas here neccessary to load the data, or are there better
    # ways to check the equality of data?
