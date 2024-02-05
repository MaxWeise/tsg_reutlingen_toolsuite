"""Define a test suit to test methods that write excel files.

Created: 03.02.2024
@author: Max Weise
"""
# pylint: disable=redefined-outer-name

import os
import pathlib

import pytest
from saison_kickstarter import excel_file_writer


@pytest.fixture
def testfile():
    """The name of the created file."""
    return pathlib.Path("./test_excel_file.xlsx")


@pytest.fixture
def testdata():
    """The name of the created file."""
    return [
        ("01.01.2000", "RL-U11 Reutlingen", False),
        ("01.01.2000", "RL-U11 Reutlingen", False),
        ("01.01.2000", "RL-U11 Reutlingen", False),
        ("01.01.2000", "RL-U11 Reutlingen", False),
    ]


def test_write_excel_file(testfile, testdata):
    """Test that an excel file is written to disk."""
    under_test = excel_file_writer.ExcelFileWriter()

    under_test.write_file(testfile, testdata)

    assert testfile.exists()

    if testfile.exists():
        os.remove(testfile)
