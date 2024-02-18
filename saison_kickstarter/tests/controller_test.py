"""Define a test suite for the functions of the system controller.

Created: 07.02.2024
@author: Max Weise
"""
# pylint: disable=redefined-outer-name

import pytest

from saison_kickstarter.controller import create_tournament_overview
from saison_kickstarter.database import Database
from saison_kickstarter.excel_file_writer import ExcelFileWriter
from saison_kickstarter.view_builder import ViewBuilder
import tests.mock_classes


@pytest.fixture
def test_data_source() -> Database:
    return tests.mock_classes.MockDatabase()


@pytest.fixture
def test_view_builder() -> ViewBuilder:
    return tests.mock_classes.MockViewBuilder()


@pytest.fixture
def test_excel_file_writer() -> ExcelFileWriter:
    return tests.mock_classes.MockFileWriter()


def test_create_tournament_overview(
    test_data_source, test_view_builder, test_excel_file_writer
):
    """Create an overview of all tournaments of a season."""
    actual = create_tournament_overview(
        test_data_source,
        test_view_builder,
        test_excel_file_writer
    )

    assert actual


def test_read_tournaments_from_file():
    """Read tournament entries from a given file."""
    ...
