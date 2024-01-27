"""Tests for the View-builder class.

Created: 27.01.2024
@author: Max Weise
"""
# pylint: disable=redefined-outer-name

import datetime

import pytest
from saison_kickstarter.tournament import AgeGroup, Category, Tournament
from saison_kickstarter.view_builder import ViewBuilder


@pytest.fixture
def test_tournaments_u11() -> list[Tournament]:
    """A list of tournaments to test against."""
    tournaments = [
        Tournament(
            1,
            datetime.date(2000, 1, 1),
            "Reutlingen",
            Category.RL,
            {AgeGroup.U11},
        ),
        Tournament(
            2,
            datetime.date(2000, 1, 1),
            "Reutlingen",
            Category.RL,
            {AgeGroup.U11},
        ),
        Tournament(
            3,
            datetime.date(2000, 1, 1),
            "Reutlingen",
            Category.RL,
            {AgeGroup.U11},
        ),
        Tournament(
            4,
            datetime.date(2000, 1, 1),
            "Reutlingen",
            Category.RL,
            {AgeGroup.U11},
        ),
    ]

    return tournaments


def test_build_block_u11_tournaments(test_tournaments_u11):
    under_test = ViewBuilder()
    under_test.set_tournaments_u11(test_tournaments_u11)

    actual = under_test.build_block(AgeGroup.U11)

    expected = [
        ("01.01.2000", "RL-U11 Reutlingen"),
        ("01.01.2000", "RL-U11 Reutlingen"),
        ("01.01.2000", "RL-U11 Reutlingen"),
        ("01.01.2000", "RL-U11 Reutlingen"),
    ]

    assert actual == expected
