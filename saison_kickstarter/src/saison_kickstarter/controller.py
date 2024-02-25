"""Define functions that map to use cases of the system

Created: 07.02.2024
@author: Max Weise
"""

import pathlib

from saison_kickstarter.database import Database
from saison_kickstarter.view_builder import ViewBuilder
from saison_kickstarter.excel_file_writer import ExcelFileWriter
from saison_kickstarter.tournament import Tournament


def create_tournament_overview(
    overview_file: pathlib.Path,
    data_source: Database,
    view_builder: ViewBuilder,
    file_writer: ExcelFileWriter
) -> None:
    """Create an overview of all tournaments of a season.

    Args:
        overview_file: Path to the file containing the overview.
        data_source: The data that is shown in the overview. Can be a database
        or a file.

    Raises:
        ValueError: No values in the database are found.
    """
    tournaments: list[Tournament] | None = data_source.read()

    if not tournaments:
        raise ValueError("There are no values in the Database!")

    tournament_view = view_builder.build_tournament_overview(tournaments)
    file_writer.write_tournament_overview(
        overview_file,
        tournament_view,
        row=2,
        col=3
    )


def read_tournaments_from_file() -> None:
    """Read tournament entries from a given file."""
    pass
