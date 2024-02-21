"""Tests for the View-builder class.

Created: 27.01.2024
@author: Max Weise
"""
# pylint: disable=redefined-outer-name

import datetime

import pytest
from saison_kickstarter.tournament import AgeGroup, Category, Tournament
from saison_kickstarter.excel_view_builder import ExcelViewBuilder


@pytest.fixture
def test_tournaments() -> list[Tournament]:
    """A list of tournaments to test against."""
    tournaments = [
        Tournament(
            1,
            datetime.date(2000, 1, 1),
            "Reutlingen",
            Category.RL,
            AgeGroup.U11,
        ),
        Tournament(
            2,
            datetime.date(2000, 2, 1),
            "Reutlingen",
            Category.RL,
            AgeGroup.U13,
        ),
        Tournament(
            3,
            datetime.date(2000, 3, 1),
            "Reutlingen",
            Category.RL,
            AgeGroup.U15,
        ),
        Tournament(
            4,
            datetime.date(2000, 4, 1),
            "Reutlingen",
            Category.RL,
            AgeGroup.U11,
        ),
    ]

    return tournaments


def test_build_block_u11_tournaments(test_tournaments):
    under_test = ExcelViewBuilder()
    actual = under_test.build_tournament_overview(test_tournaments)

    expected = [
        ("01.01.2000", "RL-U11 Reutlingen", False),
        ("01.04.2000", "RL-U11 Reutlingen", False),
        ("01.02.2000", "RL-U13 Reutlingen", False),
        ("01.03.2000", "RL-U15 Reutlingen", True),
        ("01.03.2000", "RL-U15 Reutlingen", False),
    ]

    assert actual == expected
