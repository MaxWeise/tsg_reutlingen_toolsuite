"""Define a test suit to test methods that write excel files.

Created: 03.02.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

from datetime import date

import pandas as pd
import pytest
from saison_kickstarter.view_item import RefereeViewItem, TournamentViewItem

from saison_kickstarter import file_writer, tournament

# TODO: Test Fixtures anpassen


@pytest.fixture
def testfile(tmp_path):
    """Temporary file provided by pytest."""
    tmp_file = tmp_path / "test_excel_file.xlsx"
    return tmp_file


@pytest.fixture
def test_tournament_view_items() -> list[TournamentViewItem]:
    """Testdata to write in the temporary file."""
    return [
        TournamentViewItem(
            tournament.Tournament(
                first_day=date(2000, 1, 1),
                second_day=date(2000, 1, 2),
                city="Reutlingen",
                category=tournament.category_from_string("RL"),
                age_group=tournament.age_group_from_string("U13"),
            ),
            False
        ),
        TournamentViewItem(
            tournament.Tournament(
                first_day=date(2000, 1, 1),
                second_day=date(2000, 1, 2),
                city="Reutlingen",
                category=tournament.category_from_string("RL"),
                age_group=tournament.age_group_from_string("U13"),
            ),
            False
        ),
        TournamentViewItem(
            tournament.Tournament(
                first_day=date(2000, 1, 1),
                second_day=date(2000, 1, 2),
                city="Reutlingen",
                category=tournament.category_from_string("RL"),
                age_group=tournament.age_group_from_string("U13"),
            ),
            False
        ),
        TournamentViewItem(
            tournament.Tournament(
                first_day=date(2000, 1, 1),
                second_day=date(2000, 1, 2),
                city="Reutlingen",
                category=tournament.category_from_string("RL"),
                age_group=tournament.age_group_from_string("U13"),
            ),
            True
        ),
    ]


def test_write_tournament_overview(testfile, test_tournament_view_items):
    """Test that an excel file is written to disk."""
    under_test = file_writer.ExcelFileWriter(testfile)

    under_test.write_tournament_data(test_tournament_view_items)

    assert testfile.exists()

    table = pd.read_excel(testfile)
    assert len(table.index) == len(test_tournament_view_items)


@pytest.fixture
def test_referee_view_items() -> list[RefereeViewItem]:
    """Testdata to write in the temporary file."""
    return [
        RefereeViewItem(date(2000, 1, 1).strftime("dd.mm.yyyy"), "Heidenheim", "E/D"),
        RefereeViewItem(date(2000, 1, 2).strftime("dd.mm.yyyy"), "Heidenheim", "E/D"),
        RefereeViewItem(date(2000, 3, 1).strftime("dd.mm.yyyy"), "Backnang", "D"),
        RefereeViewItem(date(2000, 3, 2).strftime("dd.mm.yyyy"), "Backnang", "D"),
        RefereeViewItem(date(2000, 4, 1).strftime("dd.mm.yyyy"), "Heidelberg", "E/D"),
        RefereeViewItem(date(2000, 4, 2).strftime("dd.mm.yyyy"), "Heidelberg", "E/D"),
    ]


def test_write_referee_overview(testfile, test_referee_view_items):
    """Test that an excel file is written to disk."""
    test_data = test_referee_view_items
    under_test = file_writer.ExcelFileWriter(testfile)

    under_test.write_referee_data(test_data)

    assert testfile.exists()

    table = pd.read_excel(testfile)
    assert len(table.index) == len(test_data)
