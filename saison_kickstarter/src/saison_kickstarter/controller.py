"""Define functions that map to use cases of the system

Created: 07.02.2024
@author: Max Weise
"""

import pathlib

from saison_kickstarter import exceptions, tournament
from saison_kickstarter.database.database import Database
from saison_kickstarter.file_reader.file_reader import FileReader
from saison_kickstarter.file_writer.excel_file_writer import ExcelFileWriter
from saison_kickstarter.view_builder.view_builder import ViewBuilder


def _check_for_duplicated_entries(data: list[tournament.Tournament]) -> bool:
    """Check if the list contains duplicated data."""
    data_as_set = set(data)
    return len(data) != len(data_as_set)


def create_tournament_overview(
    overview_file: pathlib.Path,
    data_source: Database,
    view_builder: ViewBuilder,
    file_writer: ExcelFileWriter,
) -> None:
    """Create an overview of all tournaments of a season.

    Args:
        overview_file: Path to the file containing the overview.
        data_source: The data that is shown in the overview. Can be a database
        or a file.

    Raises:
        ValueError: No values in the database are found.
    """
    tournaments: list[tournament.Tournament] | None = data_source.read()

    if not tournaments:
        raise ValueError("There are no values in the Database!")

    tournament_view = view_builder.build_tournament_overview(tournaments)
    file_writer.write_tournament_overview(
        overview_file, tournament_view, row=2, col=3
    )


def read_tournaments_from_file(
    file_reader: FileReader, data_repository: Database
) -> None:
    """Read tournament entries from a given file."""
    try:
        data = file_reader.read_data()
        tournament_data: list[tuple[str, str, str, str]] = data
    except (
        FileNotFoundError,
        ValueError,
        exceptions.FileEncodingError,
    ) as exinfo:
        raise exceptions.FileReadError(exinfo) from exinfo

    tournaments: list[tournament.Tournament] = [
        tournament.tournament_from_tuple(t) for t in tournament_data
    ]

    duplicates = _check_for_duplicated_entries(tournaments)
    if duplicates:
        raise exceptions.DuplicateEntryError(
            "There are duplicated entries in the list!"
        )

    for competition in tournaments:
        data_repository.create(item=competition)
