"""Tests for the Tournament class.

Created: 27.01.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

from datetime import date

import pytest

from saison_kickstarter.tournament import (AgeGroup, Category, Tournament,
                                           tournament_from_tuple)

standart_date = date(2000, 1, 1)


@pytest.mark.parametrize(
    ("tournament", "expected_title"),
    [
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.RL,
                age_group=AgeGroup.U11,
            ),
            "RL-U11 Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.BNWM,
                age_group=AgeGroup.U11,
            ),
            "BNWM U11 Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.RL,
                age_group=AgeGroup.U13,
            ),
            "RL-U13 Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.BNWM,
                age_group=AgeGroup.U13,
            ),
            "BNWM U13 Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.DM,
                age_group=AgeGroup.U13,
            ),
            "DM U13 Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.RL,
                age_group=AgeGroup.U15,
            ),
            "RL-U15 Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.BNWM,
                age_group=AgeGroup.U15,
            ),
            "BNWM U15 Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.QB,
                age_group=AgeGroup.U15,
            ),
            "U15Q Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.DM,
                age_group=AgeGroup.U15,
            ),
            "DM U15 Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.RL,
                age_group=AgeGroup.U17,
            ),
            "RL-U17 Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.BNWM,
                age_group=AgeGroup.U17,
            ),
            "BNWM U17 Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.QB,
                age_group=AgeGroup.U17,
            ),
            "U17Q Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.DM,
                age_group=AgeGroup.U17,
            ),
            "DM U17 Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.RL,
                age_group=AgeGroup.U20,
            ),
            "RL-U20 Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.BNWM,
                age_group=AgeGroup.U20,
            ),
            "BNWM U20 Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.QB,
                age_group=AgeGroup.U20,
            ),
            "U20Q Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.DM,
                age_group=AgeGroup.U20,
            ),
            "DM U20 Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.BNWM,
                age_group=AgeGroup.SENIOR,
            ),
            "BNWM Sen Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.QB,
                age_group=AgeGroup.SENIOR,
            ),
            "QB Reutlingen",
        ),
        (
            Tournament(
                first_day=standart_date,
                second_day=standart_date,
                city="Reutlingen",
                category=Category.DM,
                age_group=AgeGroup.SENIOR,
            ),
            "DM Sen Reutlingen",
        ),
    ],
)
def test_get_title(tournament, expected_title):
    """Test the correct contruction of the tournament title."""

    under_test = tournament
    actual = under_test.title
    expected = expected_title

    assert actual == expected


@pytest.mark.parametrize(
    ("data", "expected_tournament"),
    [
        (
            ("01./02.01.2000", "Reutlingen", "RL", "U11"),
            Tournament(
                first_day=date(2000, 1, 1),
                second_day=date(2000, 1, 2),
                city="Reutlingen",
                category=Category.RL,
                age_group=AgeGroup.U11,
            ),
        ),
        (
            ("31.01./01.02.2000", "Reutlingen", "RL", "U11"),
            Tournament(
                first_day=date(2000, 1, 31),
                second_day=date(2000, 2, 1),
                city="Reutlingen",
                category=Category.RL,
                age_group=AgeGroup.U11,
            ),
        ),
    ],
)
def test_tournament_from_tuple(data, expected_tournament):
    """Test for the tournament_from_tuple method."""
    test_data = data
    actual = tournament_from_tuple(test_data)

    assert actual == expected_tournament
