"""An interface to write data to files.

The file-writer interface encapsules common attributes and operations
to handle a datasource and writing data to it.


Created: 11.04.2025
@author: Max Weise
"""

import io
import pathlib
from typing import Protocol, Sequence

import xlsxwriter  # type: ignore
import xlsxwriter.exceptions  # type: ignore

from saison_kickstarter import exceptions, view_item


class FileWriter(Protocol):
    """Write content to files."""

    def write_tournament_data(
        self, data: Sequence[view_item.ViewItem], row: int = 0, col: int = 0
    ) -> None:
        """Create a structured tournament overview in a (temporary) file object."""
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )

    def write_referee_data(
        self, data: list[view_item.ViewItem], row: int = 0, col: int = 0
    ) -> None:
        """Create a structured referee overview in a (temporary) file object."""
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )


class ExcelFileWriter:
    """Provide an interface to write data to an excel file.

    Attributes:
        destination (pathlib.Path | io.BytesIO): The destination to write the
            data to. In case of a path, an excel file will be created. In case
            of buffer object, the buffer will be modified and can be worked
            with later on.
    """

    def __init__(self, destination: pathlib.Path | io.BytesIO) -> None:
        self.destination = destination

    def write_tournament_data(
        self,
        data: Sequence[view_item.ViewItem],
        row: int = 0,
        col: int = 0,
    ) -> None:
        """Write an overview of tournaments to an excel file.

        Args:
            data (list[ViewItem]): List of entries that get written to the file.
            row (int): Starting row in the excel workbook. Defaults to 0.
            col (int): Starting col in the excel workbook. Defaults to 0.

        Raises:
            exceptions.WorkbookError: The active workbook encountered a
                problem. Contains further information about the error.
        """
        workbook = xlsxwriter.Workbook(self.destination)

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

        for obj in data:
            date, title, is_optional = obj.to_tuple()
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

    def write_referee_data(
        self,
        data: Sequence[view_item.ViewItem],
        row: int = 0,
        col: int = 0,
    ) -> None:
        """Write an overview of referees to an excel file.

        Args:
            data (list[ViewItem]): List of entries that get written to the file.
            row (int): Starting row in the excel workbook. Defaults to 0.
            col (int): Starting col in the excel workbook. Defaults to 0.

        Raises:
            exceptions.WorkbookError: The active workbook encountered a
                problem. Contains further information about the error.
        """
        workbook = xlsxwriter.Workbook(self.destination)

        try:
            tournament_worksheet = workbook.add_worksheet(
                "Kampfrichterübersicht"
            )
        except (
            xlsxwriter.exceptions.InvalidWorksheetName,
            xlsxwriter.exceptions.DuplicateWorksheetName,
        ) as exinfo:
            raise exceptions.WorkbookError from exinfo

        for offset, header in enumerate(
            ["Datum", "Turnier", "Lizenz", "1", "2", "3"]
        ):
            tournament_worksheet.write(row, col + offset, header)

        row += 1

        for obj in data:
            day, city, required_license = obj.to_tuple()
            tournament_worksheet.write_string(
                row,
                col,
                day,
            )

            tournament_worksheet.write_string(
                row,
                col + 1,
                city,
            )

            tournament_worksheet.write_string(
                row,
                col + 2,
                required_license,
            )
            row = row + 1

        workbook.close()
