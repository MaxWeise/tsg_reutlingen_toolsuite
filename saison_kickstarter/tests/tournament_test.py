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
