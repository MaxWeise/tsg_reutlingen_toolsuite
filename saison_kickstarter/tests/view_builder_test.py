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
            first_day=datetime.date(2000, 1, 1),
            second_day=datetime.date(2000, 1, 2),
            city="Reutlingen",
            category=tournament.Category.RL,
            age_group=tournament.AgeGroup.U17,
        ),
        tournament.Tournament(
            first_day=datetime.date(2000, 2, 1),
            second_day=datetime.date(2000, 2, 2),
            city="Reutlingen",
            category=tournament.Category.RL,
            age_group=tournament.AgeGroup.U15,
        ),
        tournament.Tournament(
            first_day=datetime.date(2000, 3, 1),
            second_day=datetime.date(2000, 3, 2),
            city="Reutlingen",
            category=tournament.Category.RL,
            age_group=tournament.AgeGroup.U13,
        ),
        tournament.Tournament(
            first_day=datetime.date(2000, 4, 1),
            second_day=datetime.date(2000, 4, 2),
            city="Reutlingen",
            category=tournament.Category.RL,
            age_group=tournament.AgeGroup.U11,
        ),
        tournament.Tournament(
            first_day=datetime.date(2000, 5, 1),
            second_day=datetime.date(2000, 5, 2),
            city="Reutlingen",
            category=tournament.Category.RL,
            age_group=tournament.AgeGroup.U20,
        ),
        tournament.Tournament(
            first_day=datetime.date(2000, 6, 1),
            second_day=datetime.date(2000, 6, 2),
            city="Reutlingen",
            category=tournament.Category.QB,
            age_group=tournament.AgeGroup.SENIOR,
        ),
        tournament.Tournament(
            first_day=datetime.date(2000, 7, 31),
            second_day=datetime.date(2000, 8, 1),
            city="Reutlingen",
            category=tournament.Category.QB,
            age_group=tournament.AgeGroup.SENIOR,
        ),
    ]
    return test_tournaments


def test_build_tournament_overview(test_tournaments):
    """Test for the build_tournament_overview method.

    Given a list of tournaments, that have dfferent age groups.
    When assembling blocks of tournaments
    Then the resulting list should be sorted by date.
    """
    under_test = excel_view_builder.TournamentViewBuilder()
    actual = under_test.build_view(test_tournaments)

    expected = [
        # U11 Tournaments
        ("01./02.04.2000", "RL-U11 Reutlingen", False),
        # U13 Tournaments with optional U15 Tournaments
        ("01./02.02.2000", "RL-U15 Reutlingen", True),
        ("01./02.03.2000", "RL-U13 Reutlingen", False),
        # U15 Tournaments with optional U17 Tournaments
        ("01./02.01.2000", "RL-U17 Reutlingen", True),
        ("01./02.02.2000", "RL-U15 Reutlingen", False),
        # U17 Tournaments with optional U20 Tournaments
        ("01./02.01.2000", "RL-U17 Reutlingen", False),
        ("01./02.05.2000", "RL-U20 Reutlingen", True),
        # U20 Tournaments with optional Senior Tournaments
        ("01./02.05.2000", "RL-U20 Reutlingen", False),
        ("01./02.06.2000", "QB Reutlingen", True),
        ("31.07./01.08.2000", "QB Reutlingen", True),
        # Senior Tournaments
        ("01./02.06.2000", "QB Reutlingen", False),
        ("31.07./01.08.2000", "QB Reutlingen", False),
    ]

    assert actual == expected


def test_build_tournament_overview_without_optional_tournaments(
    test_tournaments,
):
    """Test for the build_tournament_overview method.

    Given a list of tournaments, that have different age groups,
    When assembling blocks of tournaments and a flag to exclude optional
        tourmanets is set to false
    Then the resulting list should be sorted by date and only mandatory
        tournaments should be included.
    """

    under_test = excel_view_builder.TournamentViewBuilder()
    actual = under_test.build_view(
        test_tournaments, include_optional_tournaments=False
    )

    expected = [
        # U11 Tournaments
        ("01./02.04.2000", "RL-U11 Reutlingen", False),
        # U13 Tournaments with optional U15 Tournaments
        ("01./02.03.2000", "RL-U13 Reutlingen", False),
        # U15 Tournaments with optional U17 Tournaments
        ("01./02.02.2000", "RL-U15 Reutlingen", False),
        # U17 Tournaments with optional U20 Tournaments
        ("01./02.01.2000", "RL-U17 Reutlingen", False),
        # U20 Tournaments with optional Senior Tournaments
        ("01./02.05.2000", "RL-U20 Reutlingen", False),
        # Senior Tournaments
        ("01./02.06.2000", "QB Reutlingen", False),
        ("31.07./01.08.2000", "QB Reutlingen", False),
    ]

    assert actual == expected
