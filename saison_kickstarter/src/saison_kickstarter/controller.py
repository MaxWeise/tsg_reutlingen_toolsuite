"""Define functions that map to use cases of the system

Created: 07.02.2024
@author: Max Weise
"""

import saison_kickstarter.database
from saison_kickstarter.database import Database
from saison_kickstarter.view_builder import ViewBuilder
from saison_kickstarter.excel_file_writer import ExcelFileWriter


def create_tournament_overview(
    data_source: Database,
    view_builder: ViewBuilder,
    file_writer: ExcelFileWriter
) -> None:
    """Create an overview of all tournaments of a season."""


def read_tournaments_from_file() -> None:
    """Read tournament entries from a given file."""
    ...
