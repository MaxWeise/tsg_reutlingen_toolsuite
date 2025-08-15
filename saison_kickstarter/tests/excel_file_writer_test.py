"""Define a test suit to test methods that write excel files.

Created: 03.02.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

import io
from datetime import date

import numpy
import pandas as pd
import pytest

from saison_kickstarter import file_writer
from saison_kickstarter.view_item import RefereeViewItem, TournamentViewItem


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
            date(2000, 1, 1),
            date(2000, 1, 2),
            "RL-U13 Reutlingen",
            False
        ),
        TournamentViewItem(
            date(2000, 1, 1),
            date(2000, 1, 2),
            "RL-U13 Reutlingen",
            False
        ),
        TournamentViewItem(
            date(2000, 1, 1),
            date(2000, 1, 2),
            "RL-U13 Reutlingen",
            False
        ),
        TournamentViewItem(
            date(2000, 1, 1),
            date(2000, 1, 2),
            "RL-U13 Reutlingen",
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


def test_write_tournament_overview_with_buffer_object(test_tournament_view_items) -> None:
    """Test the functionality of the method when passing a buffer object to the class.

    To be 100 % sure of the correctness of the data in the buffer, it would be
    necessary to convert the expected contents of the buffer to a bytes
    representation and compare the data against the contents of the buffer.
    However, as the code to writer to an exel file and the code to write to the
    buffer object are identical, we just assume the method to work correctly,
    as long as there is _any_ data in the buffer. This method is simpler,
    although not fully correct.
    """
    with io.BytesIO() as test_buffer:
        under_test = file_writer.ExcelFileWriter(test_buffer)
        under_test.write_tournament_data(test_tournament_view_items)
        assert test_buffer.getvalue() 


@pytest.fixture
def test_referee_view_items() -> list[RefereeViewItem]:
    """Testdata to write in the temporary file."""
    return [
        RefereeViewItem(date(2000, 1, 1), "Heidenheim", "E/D"),
        RefereeViewItem(date(2000, 1, 2), "Heidenheim", "E/D"),
        RefereeViewItem(date(2000, 3, 1), "Backnang", "D"),
        RefereeViewItem(date(2000, 3, 2), "Backnang", "D"),
        RefereeViewItem(date(2000, 4, 1), "Heidelberg", "E/D"),
        RefereeViewItem(date(2000, 4, 2), "Heidelberg", "E/D"),
    ]


def test_write_referee_overview(testfile, test_referee_view_items):
    """Test that an excel file is written to disk."""
    test_data = test_referee_view_items
    under_test = file_writer.ExcelFileWriter(testfile)

    under_test.write_referee_data(test_data)

    assert testfile.exists()

    expected = pd.DataFrame(data={
        "Datum": ["01.01.2000", "02.01.2000", "01.03.2000","02.03.2000","01.04.2000","02.04.2000"],
        "Turnier": ["Heidenheim", "Heidenheim", "Backnang", "Backnang", "Heidelberg", "Heidelberg"],
        "Lizenz": ["E/D", "E/D", "D", "D", "E/D", "E/D"],
        "1": [numpy.nan, numpy.nan, numpy.nan, numpy.nan, numpy.nan, numpy.nan],
        "2": [numpy.nan, numpy.nan, numpy.nan, numpy.nan, numpy.nan, numpy.nan],
        "3": [numpy.nan, numpy.nan, numpy.nan, numpy.nan, numpy.nan, numpy.nan],
    })

    table = pd.read_excel(testfile)
    assert len(table.index) == len(test_data)
    assert table.equals(expected)
