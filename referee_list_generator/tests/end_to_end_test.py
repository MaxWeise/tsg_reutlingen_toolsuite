"""End to end tests for the script.

Tests in this file are more or less a way of asserting, that the scrpt runs
without crashing or does not start on wrong inputs.

Created: 23.12.2023
@author: Max Weise
"""

import os
import pathlib

import pytest
from referee_list_generator.main import main  # type: ignore
from referee_list_generator.system_core import MissingArgumentError


@pytest.fixture
def test_file_utf8() -> str:
    """The testfile for all standard tests."""
    return "tests/test_assets/new_testfile_referees.csv"


@pytest.fixture
def excel_file() -> pathlib.Path:
    """The output excel file."""
    return pathlib.Path("./output_file.xlsx")


def test_main_no_file_name_given():
    """When no filename is given raise a ValueError."""
    with pytest.raises(MissingArgumentError) as error:
        main(csv_filename=None)
        assert "filename is missing" in str(error.value)


def test_create_excel_file(test_file_utf8, excel_file) -> None:
    """When given a csv file, create a non-empty excel file."""
    test_excel_file: pathlib.Path = excel_file
    actual: bool | None = main(csv_filename=test_file_utf8, excel_file=test_excel_file)

    assert actual

    if test_excel_file.exists():
        os.remove(test_excel_file)
