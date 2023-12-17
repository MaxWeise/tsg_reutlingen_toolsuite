"""Test suite for functions that write data to disk.

Created: 13.12.2023
@author: Max Weise
"""

import os
import pathlib

import pytest
from src.referee_list_generator.main import DataRow, write_data_to_excel_file


@pytest.fixture
def test_data() -> list[DataRow]:
    """Test data to be written to an excel file."""
    rv: list[DataRow] = [
        DataRow("Weise", "Max", "2001", training_D_licence=True),
        DataRow("Mustermann", "Max", "1980"),
        DataRow("Henry", "Henryson", "2020"),
        DataRow("Jürgen", "Hurenson", "1969"),
    ]
    return rv


def test_write_data_to_excel_file(test_data):
    """Check that the excel file is created and contains the correct data."""
    test_file = pathlib.Path("./test_file.xlsx")
    data = test_data
    actual = write_data_to_excel_file(data, test_file)

    assert actual
    assert test_file.exists()

    if test_file.exists():
        os.remove(test_file)
