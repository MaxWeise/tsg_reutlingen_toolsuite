"""Test functions that read from files.

Created: 30.10.2023
@author: Max Weise
"""
# pylint: disable=redefined-outer-name

import pathlib

import pytest
from referee_list_generator.functions import read_csv_file  # type: ignore

_TABEL_HEADERS = (
    "id",
    "lastname",
    "firstname",
    "dateofbirth",
    "nation",
    "nationality1",
    "nationality2",
    "club_id",
    "clubname",
    "gender",
    "addressStreet",
    "addressPostcode",
    "addressCity",
    "addressCountry",
)
_FIRST_ROW = (
    "201156",
    "Mayer",
    "Olaf",
    "01.01.1972",
    "GER",
    "GER",
    "",
    "350",
    "TSG Hauptverein",
    "M",
    "Feldweg 13/5",
    "72795",
    "Hauptstadt",
    "Deutschland",
)


@pytest.fixture
def test_file_utf8() -> pathlib.Path:
    """The testfile for all standard tests."""
    return pathlib.Path("tests/test_assets/new_testfile_referees.csv")


@pytest.fixture
def test_file_utf16() -> pathlib.Path:
    """The testfile in an unsupported file encoding."""
    return pathlib.Path("tests/test_assets/testfile_referees.csv")


def test_read_csv_file(test_file_utf8):
    """Test that a file is corectly read."""
    return_value = read_csv_file(test_file_utf8)

    assert return_value is not None
    assert len(return_value) == 8
    assert return_value[0] == _TABEL_HEADERS
    assert return_value[1] == _FIRST_ROW


def test_read_csv_file_wrong_file_encoding(test_file_utf16):
    """Given a file with wrong encoding, an error should be thrown."""
    return_value = read_csv_file(test_file_utf16)
    assert return_value is None


def test_read_csv_file_path_does_not_exist():
    """Return None when a path does not exist."""
    under_test = read_csv_file(pathlib.Path("./thisPathDoesNotExist.txt"))
    assert under_test is None
