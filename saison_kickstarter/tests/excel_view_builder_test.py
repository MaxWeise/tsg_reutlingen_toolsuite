"""Tests for the View-builder class.

Created: 27.01.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

import datetime
from datetime import date

import pytest

from saison_kickstarter import tournament, view_builder
from saison_kickstarter.view_item import RefereeViewItem, ViewItem


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


def test_build_referee_overview(test_tournaments) -> None:
    """Test for the build_referee_view method.

    Given a list of tournaments,
    When calling the tested method,
    Then an overview of all tournament days should be returned. Each tournament
        is split in two sepreate entries and each entry has a licence
        associated to it. Tournaments with category QB or with city Reutlingen
        should not be included.
    """
    test_tournaments = [
        tournament.Tournament(
            first_day=datetime.date(2000, 1, 1),
            second_day=datetime.date(2000, 1, 2),
            city="Heidenheim",
            category=tournament.Category.RL,
            age_group=tournament.AgeGroup.U11,
        ),
        tournament.Tournament(
            first_day=datetime.date(2000, 2, 1),
            second_day=datetime.date(2000, 2, 2),
            city="Reutlingen",
            category=tournament.Category.RL,
            age_group=tournament.AgeGroup.U11,
        ),
        tournament.Tournament(
            first_day=datetime.date(2000, 3, 1),
            second_day=datetime.date(2000, 3, 2),
            city="Backnang",
            category=tournament.Category.RL,
            age_group=tournament.AgeGroup.U17,
        ),
        tournament.Tournament(
            first_day=datetime.date(2000, 4, 1),
            second_day=datetime.date(2000, 4, 2),
            city="Heidelberg",
            category=tournament.Category.RL,
            age_group=tournament.AgeGroup.U13,
        ),
        tournament.Tournament(
            first_day=datetime.date(2000, 4, 1),
            second_day=datetime.date(2000, 4, 2),
            city="Heidelberg",
            category=tournament.Category.QB,
            age_group=tournament.AgeGroup.SENIOR,
        ),
        tournament.Tournament(
            first_day=datetime.date(2000, 4, 1),
            second_day=datetime.date(2000, 4, 2),
            city="Heidelberg",
            category=tournament.Category.DM,
            age_group=tournament.AgeGroup.U13,
        ),
    ]
    under_test = excel_view_builder.ExcelViewBuilder()
    actual = under_test.build_referee_view(test_tournaments)

    # List is smaller, because not every tournament needs to be included
    expected = [
        RefereeViewItem(datetime.date(2000, 1, 1), "Heidenheim", "E/D"),
        RefereeViewItem(datetime.date(2000, 1, 2), "Heidenheim", "E/D"),
        RefereeViewItem(datetime.date(2000, 3, 1), "Backnang", "D"),
        RefereeViewItem(datetime.date(2000, 3, 2), "Backnang", "D"),
        RefereeViewItem(datetime.date(2000, 4, 1), "Heidelberg", "E/D"),
        RefereeViewItem(datetime.date(2000, 4, 2), "Heidelberg", "E/D"),
    ]

    assert actual == expected
