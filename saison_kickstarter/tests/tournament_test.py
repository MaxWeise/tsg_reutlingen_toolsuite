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
            Tournament(standart_date, "Reutlingen", Category.RL, AgeGroup.U11),
            "RL-U11 Reutlingen",
        ),
        (
            Tournament(
                standart_date, "Reutlingen", Category.BNWM, AgeGroup.U11
            ),
            "BNWM U11 Reutlingen",
        ),
        (
            Tournament(standart_date, "Reutlingen", Category.RL, AgeGroup.U13),
            "RL-U13 Reutlingen",
        ),
        (
            Tournament(
                standart_date, "Reutlingen", Category.BNWM, AgeGroup.U13
            ),
            "BNWM U13 Reutlingen",
        ),
        (
            Tournament(standart_date, "Reutlingen", Category.DM, AgeGroup.U13),
            "DM U13 Reutlingen",
        ),
        (
            Tournament(standart_date, "Reutlingen", Category.RL, AgeGroup.U15),
            "RL-U15 Reutlingen",
        ),
        (
            Tournament(
                standart_date, "Reutlingen", Category.BNWM, AgeGroup.U15
            ),
            "BNWM U15 Reutlingen",
        ),
        (
            Tournament(standart_date, "Reutlingen", Category.QB, AgeGroup.U15),
            "U15Q Reutlingen",
        ),
        (
            Tournament(standart_date, "Reutlingen", Category.DM, AgeGroup.U15),
            "DM U15 Reutlingen",
        ),
        (
            Tournament(standart_date, "Reutlingen", Category.RL, AgeGroup.U17),
            "RL-U17 Reutlingen",
        ),
        (
            Tournament(
                standart_date, "Reutlingen", Category.BNWM, AgeGroup.U17
            ),
            "BNWM U17 Reutlingen",
        ),
        (
            Tournament(standart_date, "Reutlingen", Category.QB, AgeGroup.U17),
            "U17Q Reutlingen",
        ),
        (
            Tournament(standart_date, "Reutlingen", Category.DM, AgeGroup.U17),
            "DM U17 Reutlingen",
        ),
        (
            Tournament(standart_date, "Reutlingen", Category.RL, AgeGroup.U20),
            "RL-U20 Reutlingen",
        ),
        (
            Tournament(
                standart_date, "Reutlingen", Category.BNWM, AgeGroup.U20
            ),
            "BNWM U20 Reutlingen",
        ),
        (
            Tournament(standart_date, "Reutlingen", Category.QB, AgeGroup.U20),
            "U20Q Reutlingen",
        ),
        (
            Tournament(standart_date, "Reutlingen", Category.DM, AgeGroup.U20),
            "DM U20 Reutlingen",
        ),
        (
            Tournament(
                standart_date, "Reutlingen", Category.BNWM, AgeGroup.SENIOR
            ),
            "BNWM Sen Reutlingen",
        ),
        (
            Tournament(
                standart_date, "Reutlingen", Category.QB, AgeGroup.SENIOR
            ),
            "QB Reutlingen",
        ),
        (
            Tournament(
                standart_date, "Reutlingen", Category.DM, AgeGroup.SENIOR
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


def test_tournament_from_tuple_table_header_senioren():
    """Test for the correct contruction of a tournament object.

    Given the age group "senioren"
    When calling the tested method
    The object should have the age group "senior".
    """
    test_tuple_en = ("21.02.2001", "Reutlingen", "RL", "senior")
    test_tuple_de = ("21.02.2001", "Reutlingen", "RL", "Senioren")

    actual_en = tournament.tournament_from_tuple(test_tuple_en)
    actual_de = tournament.tournament_from_tuple(test_tuple_de)

    assert actual_en == actual_de


def test_tournament_from_tuple_table_header_veteranen():
    """Test for the correct contruction of a tournament object.

    Given the age group "veteranen"
    When calling the tested method
    The object should have the age group "veteran".
    """
    test_tuple_en = ("21.02.2001", "Reutlingen", "RL", "veteran")
    test_tuple_de = ("21.02.2001", "Reutlingen", "RL", "Veteranen")

    actual_en = tournament.tournament_from_tuple(test_tuple_en)
    actual_de = tournament.tournament_from_tuple(test_tuple_de)

    assert actual_en == actual_de
