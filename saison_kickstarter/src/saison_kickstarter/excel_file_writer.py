"""Define a component that writes data to excel files.

Created: 03.02.2024
@author: Max Weise
"""

import pathlib
import typing

import xlsxwriter  # type: ignore

from saison_kickstarter.view_builder import OverviewEntry


class ExcelFileWriter:
    """Write date to an excel file."""

    def _write_header(
        self, worksheet: typing.Any, header_names: list[str], row: int, col: int
    ) -> None:
        """Writer the headers for a table.

        Args:
            header_names: The header names for all columns.
            row: The row position of the headers.
            col: The position of the first column.
        """

        for offset, header in enumerate(header_names):
            worksheet.write(row, col + offset, header)

    def write_tournament_overview(
        self,
        file: pathlib.Path,
        contents: OverviewEntry,
        worksheet_name: str = "Turnierübersicht",
        start_row: int = 0,
        start_col: int = 0,
    ) -> None:
        """Write a given contents to a file of specified mime-type.

        Args:
            file: The name of the file that is created.
            contents: A list of entries, that will be written in the file.
        """
        row = start_row
        column = start_col

        workbook = xlsxwriter.Workbook(file)
        tournamen_worksheet = workbook.add_worksheet(worksheet_name)
        optional_tournament_format = workbook.add_format(
            {"bg_color": "#fcd5b4"}
        )

        self._write_header(tournamen_worksheet, ["Datum", "Ort"], row, column)
        row = row + 1

        for date, title, is_optional in contents:
            tournamen_worksheet.write(
                row,
                column,
                date,
                optional_tournament_format if is_optional else None,
            )
            tournamen_worksheet.write(
                row,
                column + 1,
                title,
                optional_tournament_format if is_optional else None,
            )
            row = row + 1

        workbook.close()
