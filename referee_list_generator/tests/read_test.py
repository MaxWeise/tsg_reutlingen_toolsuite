"""Test functions that read from files.

Created: 30.10.2023
@author: Max Weise
"""

import pytest
import pathlib

from referee_list_generator.main import read_csv_file

@pytest.fixture
def test_file() -> pathlib.Path:
    return pathlib.Path("tests/test_assets/testfile_referees.csv")


def test_read_csv_file(test_file):
    """Test that a file is corectly read."""
    return_value = read_csv_file(test_file)

    assert return_value != None


