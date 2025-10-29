"""This module contains tests for the TournamentViewBuilder.

It verifies that the builder correctly transforms a list of tournaments
into a sorted and grouped list of view items, handling both mandatory
and optional tournaments.
"""

# pylint: disable=redefined-outer-name

import datetime

import pytest

from saison_kickstarter import tournament, view_builder, view_item


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
    under_test = view_builder.TournamentViewBuilder(True)
    actual = under_test.build_view(test_tournaments)

    expected = [
        # U11 Turniere
        view_item.TournamentViewItem(
            datetime.date(2000, 4, 1),
            datetime.date(2000, 4, 2),
            "RL-U11 Reutlingen",
            False,
        ),
        # U13 Turniere
        view_item.TournamentViewItem(
            datetime.date(2000, 2, 1),
            datetime.date(2000, 2, 2),
            "RL-U15 Reutlingen",
            True,
        ),
        view_item.TournamentViewItem(
            datetime.date(2000, 3, 1),
            datetime.date(2000, 3, 2),
            "RL-U13 Reutlingen",
            False,
        ),
        # U15 Turniere
        view_item.TournamentViewItem(
            datetime.date(2000, 1, 1),
            datetime.date(2000, 1, 2),
            "RL-U17 Reutlingen",
            True,
        ),
        view_item.TournamentViewItem(
            datetime.date(2000, 2, 1),
            datetime.date(2000, 2, 2),
            "RL-U15 Reutlingen",
            False,
        ),
        # U17 Turniere
        view_item.TournamentViewItem(
            datetime.date(2000, 1, 1),
            datetime.date(2000, 1, 2),
            "RL-U17 Reutlingen",
            False,
        ),
        view_item.TournamentViewItem(
            datetime.date(2000, 5, 1),
            datetime.date(2000, 5, 2),
            "RL-U20 Reutlingen",
            True,
        ),
        # U20 Turniere
        view_item.TournamentViewItem(
            datetime.date(2000, 5, 1),
            datetime.date(2000, 5, 2),
            "RL-U20 Reutlingen",
            False,
        ),
        view_item.TournamentViewItem(
            datetime.date(2000, 6, 1),
            datetime.date(2000, 6, 2),
            "QB Reutlingen",
            True,
        ),
        view_item.TournamentViewItem(
            datetime.date(2000, 7, 31),
            datetime.date(2000, 8, 1),
            "QB Reutlingen",
            True,
        ),
        # Senioren Turniere
        view_item.TournamentViewItem(
            datetime.date(2000, 6, 1),
            datetime.date(2000, 6, 2),
            "QB Reutlingen",
            False,
        ),
        view_item.TournamentViewItem(
            datetime.date(2000, 7, 31),
            datetime.date(2000, 8, 1),
            "QB Reutlingen",
            False,
        ),
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

    under_test = view_builder.TournamentViewBuilder(False)
    actual = under_test.build_view(test_tournaments)

    expected = [
        view_item.TournamentViewItem(
            datetime.date(2000, 4, 1),
            datetime.date(2000, 4, 2),
            "RL-U11 Reutlingen",
            False,
        ),
        view_item.TournamentViewItem(
            datetime.date(2000, 3, 1),
            datetime.date(2000, 3, 2),
            "RL-U13 Reutlingen",
            False,
        ),
        view_item.TournamentViewItem(
            datetime.date(2000, 2, 1),
            datetime.date(2000, 2, 2),
            "RL-U15 Reutlingen",
            False,
        ),
        view_item.TournamentViewItem(
            datetime.date(2000, 1, 1),
            datetime.date(2000, 1, 2),
            "RL-U17 Reutlingen",
            False,
        ),
        view_item.TournamentViewItem(
            datetime.date(2000, 5, 1),
            datetime.date(2000, 5, 2),
            "RL-U20 Reutlingen",
            False,
        ),
        view_item.TournamentViewItem(
            datetime.date(2000, 6, 1),
            datetime.date(2000, 6, 2),
            "QB Reutlingen",
            False,
        ),
        view_item.TournamentViewItem(
            datetime.date(2000, 7, 31),
            datetime.date(2000, 8, 1),
            "QB Reutlingen",
            False,
        ),
    ]

    assert actual == expected
