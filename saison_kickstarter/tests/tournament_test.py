"""Tests for the Tournament class.

Created: 27.01.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

from datetime import date

import pytest

from saison_kickstarter import tournament
from saison_kickstarter.tournament import AgeGroup, Category, Tournament

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


def test_tournament_from_dict():

    test_dict = {
        "first_day": "21.02.2001",
        "second_day": "22.02.2001",
        "city": "Reutlingen",
        "category": "RL",
        "age_group": "U17",
    }
    actual = tournament.tournament_from_dict(test_dict)
    expected = tournament.Tournament(
        first_day=date(day=21, month=2, year=2001),
        second_day=date(day=22, month=2, year=2001),
        city="Reutlingen",
        category=tournament.Category.RL,
        age_group=tournament.AgeGroup.U17,
    )

    assert actual == expected


def test_tournament_from_tuple_table_header_senioren():
    """Test for the correct contruction of a tournament object.

    Given the age group "senioren"
    When calling the tested method
    The object should have the age group "senior".
    """
    test_dict_de = {
        "first_day": "21.02.2001",
        "second_day": "22.02.2001",
        "city": "Reutlingen",
        "category": "RL",
        "age_group": "Senioren",
    }
    test_dict_en = {
        "first_day": "21.02.2001",
        "second_day": "22.02.2001",
        "city": "Reutlingen",
        "category": "RL",
        "age_group": "senior",
    }

    actual_en = tournament.tournament_from_dict(test_dict_de)
    actual_de = tournament.tournament_from_dict(test_dict_en)

    assert actual_en == actual_de


def test_tournament_from_tuple_table_header_veteranen():
    """Test for the correct contruction of a tournament object.

    Given the age group "veteranen"
    When calling the tested method
    The object should have the age group "veteran".
    """
    test_dict_de = {
        "first_day": "21.02.2001",
        "second_day": "22.02.2001",
        "city": "Reutlingen",
        "category": "RL",
        "age_group": "Veteranen",
    }
    test_dict_en = {
        "first_day": "21.02.2001",
        "second_day": "22.02.2001",
        "city": "Reutlingen",
        "category": "RL",
        "age_group": "veteran",
    }

    actual_en = tournament.tournament_from_dict(test_dict_en)
    actual_de = tournament.tournament_from_dict(test_dict_de)

    assert actual_en == actual_de
