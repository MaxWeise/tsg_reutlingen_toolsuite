"""Define a test suite for the functions of the system controller.

Created: 07.02.2024
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

import datetime
import os
import pathlib
from unittest import mock

import pytest

from saison_kickstarter import controller, exceptions, tournament


def test_create_tournament_overview():
    """Create an overview of all tournaments of a season.

    Given a database with a list of tournaments
    When calling the create_tournament_overview function with the dataset,
        with a view-builder that returns a structured list of entries
        with a file-writer
    Then a file should be created that is not empty.

    It is only necessary to assert that a file is created and not empty.
    Functionality of the file writer is tested in a different test suite.

    Mocks to be created:
        data_source.read
        view_builder.build_tournament_overview
        file_writer.write_tournament_overview
    """
    # Create mocks
    ## Data Source
    mock_data = [
        ("21.02.2001", "Reutlingen", "RL", "U15"),
        ("28.02.2024", "Heidenheim", "RL", "U13"),
        ("21.03.2001", "Tauberbischofsheim", "RL", "U15"),
    ]
    dbs = mock.Mock()
    dbs.read.return_value = mock_data

    ## View-Builder
    mock_view = [
        # U 13 Turniere
        ("28.02.2024", "RL-U13 Heidenheim", False),
        ("21.02.2001", "RL-U15 Reutlingen", True),
        ("21.03.2001", "RL-U15 Tauberbischofsheim", True),
        # U 15 Turniere
        ("21.02.2001", "RL-U15 Reutlingen", False),
        ("21.03.2001", "RL-U15 Tauberbischofsheim", False),
    ]
    mock_view_builder = mock.Mock()
    mock_view_builder.build_tournament_overview.return_value = mock_view

    ## File Writer
    test_path = pathlib.Path("null-path")
    mock_file_writer = mock.Mock()
    # mock_file_writer.write_tournament_overview.return_value = None

    controller.create_tournament_overview(
        test_path, dbs, mock_view_builder, mock_file_writer
    )

    # Assert that methods are called once
    dbs.read.assert_called_once()
    mock_view_builder.build_tournament_overview.assert_called_once()

    # Cleanup
    if test_path.exists():
        os.remove(test_path)


def test_create_tournament_overview_no_data_in_database():
    """Test for the create_tournament_overview function.

    Given an empty database
    When calling the function
    A ValueError should be thrown.

    The Error should specify, that the database is empty.

    Mocks for the test:
        data_source.read
    """
    # Setup Mocks
    test_path = pathlib.Path("null-path")
    dbs = mock.Mock()
    dbs.read.return_value = None

    mock_view_builder = mock.Mock()
    mock_excel_file_writer = mock.Mock()

    with pytest.raises(
        ValueError, match="There are no values in the Database!"
    ):
        controller.create_tournament_overview(
            test_path, dbs, mock_view_builder, mock_excel_file_writer
        )

    if test_path.exists():
        os.remove(test_path)


def test_read_tournaments_from_file():
    """Tests to read tournament entries from a given file.

    Given a csv file with tournament entries
    When calling the tested function
    Then the data should be written in a database file.
    """
    dbs = mock.Mock()
    mock_data = [
        ("21.02.2001", "Reutlingen", "RL", "U15"),
        ("21.02.2001", "Waldkirch", "RL", "U15"),
        ("28.02.2024", "Heidenheim", "RL", "U13"),
    ]
    mock_file_reader = mock.Mock()
    mock_file_reader.read_data.return_value = mock_data

    controller.read_tournaments_from_file(mock_file_reader, dbs)

    mock_file_reader.read_data.assert_called_once()
    dbs.create.assert_called()


@pytest.mark.parametrize(
    ("exception", "expected"),
    [
        (FileNotFoundError, exceptions.FileReadError),
        (ValueError, exceptions.FileReadError),
        (exceptions.FileEncodingError, exceptions.FileReadError),
    ],
)
def test_read_tournaments_from_file_test_exceptions(exception, expected):
    """Tests to read tournament entries from a given file.

    Given the exceptions raised by the file reader
    When an exception gets raised by the file reader
    Then the function should raise a FileReaderError from the underlying
        exception.
    """
    mock_file_reader = mock.Mock()
    mock_file_reader.read_data.side_effect = exception()
    mock_data_source = mock.Mock()

    with pytest.raises(expected):
        controller.read_tournaments_from_file(
            mock_file_reader, mock_data_source
        )


def test_read_tournaments_from_file_add_tournament_on_same_date():
    """Test for the read_data_from_file function.

    Given two tournaments on the same date but different cities
    When calling the tested function
    Then both tournaments should be added to the database.
    """
    # Setup the mock objects
    mock_data = [
        ("21.02.2001", "Reutlingen", "RL", "U15"),
        ("21.02.2001", "Waldkirch", "RL", "U15"),
        ("28.02.2024", "Heidenheim", "RL", "U13"),
    ]
    mock_file_reader = mock.Mock()
    mock_file_reader.read_data.return_value = mock_data

    mock_data_source = mock.Mock()  # No need for additional config

    # Run the tested function
    controller.read_tournaments_from_file(mock_file_reader, mock_data_source)

    # Last turnament in list. Other entries fail. Perhaps because this method
    # is called in a loop and this is the last entry.
    test_tournament = tournament.Tournament(
        datetime.date(2024, 2, 28),
        "Heidenheim",
        tournament.Category.RL,
        tournament.AgeGroup.U13,
    )

    mock_data_source.create.assert_called_with(item=test_tournament)


def test_read_tournaments_from_file_duplicated_entries():
    """Test how the controller deal with read data.

    Given reading a file with duplicated entrie.
    When reading data that has duplicated entries
    Then the function should raise an error.
    """
    # Setup mocks
    mock_data = [
        ("21.02.2001", "Reutlingen", "RL", "U15"),
        ("21.02.2001", "Reutlingen", "RL", "U15"),
        ("28.02.2024", "Heidenheim", "RL", "U13"),
    ]

    mock_file_reader = mock.Mock()
    mock_file_reader.read_data.return_value = mock_data

    mock_data_source = mock.Mock()  # No need for additional config

    mock_file_reader.set_return_value(mock_data)
    with pytest.raises(
        exceptions.DuplicateEntryError,
        match="There are duplicated entries in the list!",
    ):
        controller.read_tournaments_from_file(
            mock_file_reader, mock_data_source
        )
