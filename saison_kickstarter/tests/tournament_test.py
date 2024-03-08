"""Tests for the Tournament class.

Created: 27.01.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

from datetime import date

from saison_kickstarter import tournament


def test_get_title():
    """Test the correct contruction of the tournament title."""
    under_test = tournament.Tournament(
        date(2000, 1, 1),
        "Reutlingen",
        tournament.Category.RL,
        tournament.AgeGroup.U11,
    )

    actual = under_test.title
    expected = "RL-U11 Reutlingen"

    assert actual == expected


def test_tournament_from_tuple():

    test_tuple = ("21.02.2001", "Reutlingen", "RL", "U17")
    actual = tournament.tournament_from_tuple(test_tuple)
    expected = tournament.Tournament(
        date(day=21, month=2, year=2001),
        "Reutlingen",
        tournament.Category.RL,
        tournament.AgeGroup.U17,
    )

    assert actual == expected
