"""Define a component that writes data to excel files.

Created: 03.02.2024
@author: Max Weise
"""

import pathlib

import xlsxwriter

from saison_kickstarter.view_builder import OverviewEntry


class ExcelFileWriter:
    """Write date to an excel file."""

    def __init__(self, row: int = 0, column: int = 0) -> None:
        """Initialize a writer object an set coordinates for the cursor."""
        self.row = row
        self.column = column

    def write_tournament_overview(
        self,
        file: pathlib.Path,
        contents: OverviewEntry,
        worksheet_name: str = "Turnierübersicht",
    ) -> None:
        """Write a given contents to a file of specified mime-type.

        Args:
            file: The name of the file that is created.
            contents: A list of entries, that will be written in the file.
        """

        workbook = xlsxwriter.Workbook(file)
        tournamen_worksheet = workbook.add_worksheet(worksheet_name)

        # Ignore if tournament is optional. Use later for formatting
        # TODO: Implement coloring of optional values.
        for date, title, _ in contents:
            tournamen_worksheet.write(self.row, self.column, date)
            tournamen_worksheet.write(self.row, self.column + 1, title)
            self.row = self.row + 1

        workbook.close()
