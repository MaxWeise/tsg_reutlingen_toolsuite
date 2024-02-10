"""Define a component that writes data to excel files.

Created: 10.02.2024
@author: Max Weise
"""

import pathlib

import xlsxwriter

from saison_kickstarter.view_builder import OverviewEntry


class ExcelFileWriter:
    """Provide an interface to write data to an excel file."""

    def write_tournament_overview(
        self,
        file: pathlib.Path,
        tournaments: list[OverviewEntry],
        row: int = 0,
        col: int = 0,
    ) -> None:
        """Write an overview of tournaments to an excel file.

        Args:
            file: The path to the excel file.
            tournaments: List of entries that get written to the file.

        """
        workbook = xlsxwriter.Workbook(file)
        tournament_worksheet = workbook.add_worksheet("Turnierübersicht")
        optional_tournament_format = workbook.add_format(
            {"bg_color": "#fcd5b4"}
        )

        for offset, header in enumerate(["Datum", "Ort"]):
            tournament_worksheet.write(row, col + offset, header)

        row += 1

        for date, title, is_optional in tournaments:
            tournament_worksheet.write_string(
                row,
                col,
                date,
                optional_tournament_format if is_optional else None,
            )
            tournament_worksheet.write_string(
                row,
                col + 1,
                title,
                optional_tournament_format if is_optional else None,
            )
            row = row + 1

        workbook.close()
