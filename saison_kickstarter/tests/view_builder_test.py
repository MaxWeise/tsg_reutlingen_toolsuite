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
def test_tournaments():
    """Some tournaments to test the sorting of the list."""
    test_tournaments = [
        tournament.Tournament(
            datetime.date(2000, 1, 1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U17,
        ),
        tournament.Tournament(
            datetime.date(2000, 2, 1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U15,
        ),
        tournament.Tournament(
            datetime.date(2000, 3, 1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U13,
        ),
        tournament.Tournament(
            datetime.date(2000, 4, 1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U11,
        ),
        tournament.Tournament(
            datetime.date(2000, 5, 1),
            "Reutlingen",
            tournament.Category.RL,
            tournament.AgeGroup.U20,
        ),
        tournament.Tournament(
            datetime.date(2000, 6, 1),
            "Reutlingen",
            tournament.Category.QB,
            tournament.AgeGroup.SENIOR,
        ),
    ]
    return test_tournaments


def test_build_tournament_overview(test_tournaments):
    """Test for the build_tournament_overview method.

    Given a list of tournaments, that have dfferent age groups.
    When assembling blocks of tournaments
    Then the resulting list should be sorted by date.
    """
    under_test = excel_view_builder.ExcelViewBuilder()
    actual = under_test.build_tournament_overview(test_tournaments)

    # FIXME: Nomenclature for Senior QB should be "QB Reutlingen"
    # Instead of "QB Senior Reutlingen" (See Ticket#28)
    expected = [
        # U11 Tournaments
        ("01.04.2000", "RL-U11 Reutlingen", False),
        # U13 Tournaments with optional U15 Tournaments
        ("01.02.2000", "RL-U15 Reutlingen", True),
        ("01.03.2000", "RL-U13 Reutlingen", False),
        # U15 Tournaments with optional U17 Tournaments
        ("01.01.2000", "RL-U17 Reutlingen", True),
        ("01.02.2000", "RL-U15 Reutlingen", False),
        # U17 Tournaments with optional U20 Tournaments
        ("01.01.2000", "RL-U17 Reutlingen", False),
        ("01.05.2000", "RL-U20 Reutlingen", True),
        # U20 Tournaments with optional Senior Tournaments
        ("01.05.2000", "RL-U20 Reutlingen", False),
        ("01.06.2000", "QB Senior Reutlingen", True),
        # Senior Tournaments
        ("01.06.2000", "QB Senior Reutlingen", False),
    ]

    assert actual == expected
