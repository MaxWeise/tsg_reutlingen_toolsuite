"""Tests for the Tournament class.

Created: 27.01.2024
@author: Max Weise
"""
# pylint: disable=redefined-outer-name

from datetime import date

from saison_kickstarter.tournament import AgeGroup, Category, Tournament


def test_get_title():
    """Test the correct contruction of the tournament title."""
    under_test = Tournament(
        1, date(2000, 1, 1), "Reutlingen", Category.RL, {AgeGroup.U11}
    )

    actual = under_test.title
    expected = "RL-U11 Reutlingen"

    assert actual == expected
