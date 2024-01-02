"""Testsuite for the monad object.

Created: 02.12.2023
@author: Max Weise
"""

from referee_list_generator.system_core import Maybe


def none_function(mock_arg) -> None:
    """Return none."""
    _ = mock_arg
    return None


def add_one(number) -> int:
    """Add one to a number."""
    return number + 1


def test_maybe_returns_value():
    """Test that the maybe monad returns a value when no errors occur."""
    test_value = Maybe(0)
    first_run = test_value.bind(add_one)
    second_run = first_run.bind(add_one)
    under_test = second_run.bind(add_one)

    assert under_test.value is not None
    assert under_test.value == 3


def test_maybe_returns_none_on_error():
    """Test that the maybe monad returns none when errors occur."""
    test_value = Maybe(0)
    first_run = test_value.bind(none_function)
    second_run = first_run.bind(add_one)
    under_test = second_run.bind(add_one)

    assert under_test.value is None

    test_value = Maybe(0)
    first_run = test_value.bind(add_one)
    second_run = first_run.bind(none_function)
    under_test = second_run.bind(add_one)

    assert under_test.value is None

    test_value = Maybe(0)
    first_run = test_value.bind(add_one)
    second_run = first_run.bind(add_one)
    under_test = second_run.bind(none_function)

    assert under_test.value is None
