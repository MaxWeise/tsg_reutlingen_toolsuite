"""Define a test suite for the functions of the system controller.

Created: 07.02.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

import os
import pathlib

import pytest

import tests.mock_classes
from saison_kickstarter.controller import (
    create_tournament_overview,
    read_tournaments_from_file,
)
from saison_kickstarter.file_reader import file_reader
from saison_kickstarter.file_writer.excel_file_writer import ExcelFileWriter
from saison_kickstarter.view_builder.view_builder import ViewBuilder


@pytest.fixture()
def mock_data_source():
    return tests.mock_classes.MockDatabase


@pytest.fixture()
def mock_view_builder() -> ViewBuilder:
    return tests.mock_classes.MockViewBuilder()


@pytest.fixture()
def mock_excel_file_writer() -> ExcelFileWriter:
    return tests.mock_classes.MockFileWriter()


@pytest.fixture()
def mock_file_reader():
    return tests.mock_classes.MockFileReader("./test_assets/test_file.csv")


def test_create_tournament_overview(
    mock_data_source, mock_view_builder, mock_excel_file_writer
):
    """Create an overview of all tournaments of a season."""
    test_path = pathlib.Path("null-path")
    dbs = mock_data_source()
    create_tournament_overview(
        test_path, dbs, mock_view_builder, mock_excel_file_writer
    )

    if test_path.exists():
        os.remove(test_path)


def test_create_tournament_overview_no_data_in_database(
    mock_data_source, mock_view_builder, mock_excel_file_writer
):
    test_path = pathlib.Path("null-path")
    dbs = mock_data_source(is_empty=True)

    with pytest.raises(ValueError) as exinfo:
        create_tournament_overview(
            test_path, dbs, mock_view_builder, mock_excel_file_writer
        )
        assert "There are no values in the Database!" in str(exinfo.value)

    if test_path.exists():
        os.remove(test_path)


def test_read_tournaments_from_file(mock_file_reader, mock_data_source):
    """Read tournament entries from a given file."""
    test_path = pathlib.Path("null-path")
    dbs = mock_data_source()
    _ = read_tournaments_from_file(mock_file_reader, dbs)
