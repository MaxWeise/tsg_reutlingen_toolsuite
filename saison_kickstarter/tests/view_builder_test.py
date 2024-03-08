"""Tests for the View-builder class.

Created: 27.01.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

import datetime

import pytest

from saison_kickstarter import tournament
from saison_kickstarter.view_builder import excel_view_builder


@pytest.fixture
def test_tournaments() -> list[tournament.Tournament]:
    """A list of tournaments to test against."""
    tournaments = [
        tournament.Tournament(
            datetime.date(2000, 1, 1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U11,
        ),
        tournament.Tournament(
            datetime.date(2000, 2, 1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U13,
        ),
        tournament.Tournament(
            datetime.date(2000, 3, 1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U15,
        ),
        tournament.Tournament(
            datetime.date(2000, 4, 1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U11,
        ),
    ]

    return tournaments


def test_build_block_u11_tournaments(test_tournaments):
    under_test = excel_view_builder.ExcelViewBuilder()
    actual = under_test.build_tournament_overview(test_tournaments)

    expected = [
        ("01.01.2000", "RL-U11 Reutlingen", False),
        ("01.04.2000", "RL-U11 Reutlingen", False),
        ("01.02.2000", "RL-U13 Reutlingen", False),
        ("01.03.2000", "RL-U15 Reutlingen", True),
        ("01.03.2000", "RL-U15 Reutlingen", False),
    ]

    assert actual == expected
