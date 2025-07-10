from datetime import datetime

import pytest

from saison_kickstarter import view_item


def test_order_tournament_view_item() -> None:
    """Test that the ordering is correct."""
    view_item_one = view_item.TournamentViewItem(
        datetime(2000, 1, 1), datetime(2000, 1, 2), "RL-U11 Reutlingen", False
    )
    view_item_two = view_item.TournamentViewItem(
        datetime(2000, 1, 3), datetime(2000, 1, 4), "RL-U11 Reutlingen", False
    )

    assert view_item_one < view_item_two


@pytest.mark.parametrize(
    ("view_item", "expected_tuple"),
    [
        (
            view_item.TournamentViewItem(
                datetime(2000, 1, 1), datetime(2000, 1, 2), "RL-U11 Reutlingen", False
            ),
            ("01./02.01.2000", "RL-U11 Reutlingen", False)
        ),
        (
            view_item.TournamentViewItem(
                datetime(2000, 1, 31), datetime(2000, 2, 1), "RL-U11 Reutlingen", False
            ),
            ("31.01./01.02.2000", "RL-U11 Reutlingen", False)
        ),
    ]
)
def test_tournament_view_item_to_tuple(view_item, expected_tuple) -> None:
    """Test the correct tuple representation of an object."""
    assert view_item.to_tuple() == expected_tuple


def test_order_referee_view_item() -> None:
    """Test that the ordering is correct."""
    view_item_one = view_item.RefereeViewItem(
        datetime(2000, 1, 1), "Reutlingen", "E/D"
    )
    view_item_two = view_item.RefereeViewItem(
        datetime(2000, 1, 2), "Reutlingen", "E/D"
    )

    view_item_three = view_item.RefereeViewItem(
        datetime(2000, 2, 1), "Reutlingen", "E/D"
    )

    assert view_item_one < view_item_two < view_item_three


def test_referee_view_item_to_tuple() -> None:
    """Test the correct tuple representation of an object."""
    under_test = view_item.RefereeViewItem(datetime(2000, 1,1), "Reutlingen", "E/D")
    assert under_test.to_tuple() == ("01.01.2000", "Reutlingen", "E/D")




