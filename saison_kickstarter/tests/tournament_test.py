"""Tests for the Tournament class.

Created: 27.01.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

from datetime import date

import saison_kickstarter.tournament
from saison_kickstarter.tournament import AgeGroup, Category, Tournament


def test_get_title():
    """Test the correct contruction of the tournament title."""
    under_test = Tournament(
        date(2000, 1, 1), "Reutlingen", Category.RL, AgeGroup.U11
    )

    actual = under_test.title
    expected = "RL-U11 Reutlingen"

    assert actual == expected


def test_tournament_from_tuple():

    test_tuple = ("21.02.2001", "Reutlingen", "RL", "U17")
    actual = saison_kickstarter.tournament.tournament_from_tuple(test_tuple)
    expected = Tournament(
        date(day=21, month=2, year=2001),
        "Reutlingen",
        Category.RL,
        AgeGroup.U17,
    )

    assert actual == expected
