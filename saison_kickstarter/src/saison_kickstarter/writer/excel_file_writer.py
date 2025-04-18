"""Define a component that writes data to excel files.

Created: 10.02.2024
@author: Max Weise
"""

import pathlib

import xlsxwriter  # type: ignore
import xlsxwriter.exceptions  # type: ignore

from saison_kickstarter import exceptions


class ExcelFileWriter:
    """Provide an interface to write data to an excel file."""

    def __init__(self, data_file: pathlib.Path) -> None:
        self.data_file = data_file

    def write_data(
        self,
        data: list[tuple[str, str, bool]],
        row: int = 0,
        col: int = 0,
    ) -> None:
        """Write an overview of tournaments to an excel file.

        Args:
            file: The path to the excel file.
            tournaments: List of entries that get written to the file.

        """
        workbook = xlsxwriter.Workbook(self.data_file)

        try:
            tournament_worksheet = workbook.add_worksheet("Turnierübersicht")
        except (
            xlsxwriter.exceptions.InvalidWorksheetName,
            xlsxwriter.exceptions.DuplicateWorksheetName,
        ) as exinfo:
            raise exceptions.WorkbookError from exinfo
        optional_tournament_format = workbook.add_format(
            {"bg_color": "#fcd5b4"}
        )

        for offset, header in enumerate(["Datum", "Ort"]):
            tournament_worksheet.write(row, col + offset, header)

        row += 1

        for date, title, is_optional in data:
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
