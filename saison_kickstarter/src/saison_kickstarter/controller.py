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
        tournament_data: list[tuple[str, str, str, str]] = (
            file_reader.read_data()
        )
    except (
        FileNotFoundError | ValueError | exceptions.FileEncodingError
    ) as exinfo:
        raise exceptions.FileReadError from exinfo

    tournaments: list[tournament.Tournament] = [
        tournament.tournament_from_tuple(t) for t in tournament_data
    ]

    for competition in tournaments:
        # print(tournaments)
        print(f"\n{data_repository = } und {competition = }\n")
        success = data_repository.create(item=competition)

        if not success:
            raise exceptions.DatabaseWriteError(
                "Something went wrong while writing {competition = } to the database"
            )
