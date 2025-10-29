"""An interface to write data to files.

The file-writer interface encapsules common attributes and operations
to handle a datasource and writing data to it.


Created: 11.04.2025
@author: Max Weise
"""

import io
import pathlib
from typing import Protocol

import xlsxwriter  # type: ignore
import xlsxwriter.exceptions  # type: ignore

from saison_kickstarter import exceptions, view_item


class FileWriter(Protocol):
    """Write content to files."""

    def write_overview(
        self,
        header: list[view_item.ViewItem],
        data: list[view_item.ViewItem],
        sheet_name: str | None = None,
        row_offset: int = 0,
        col_offset: int = 0,
    ) -> None:
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

    def write_overview(
        self,
        header: list[view_item.ViewItem],
        data: list[view_item.ViewItem],
        sheet_name: str | None = None,
        row_offset: int = 0,
        col_offset: int = 0,
    ) -> None:
        """Write an overview of to an excel file.

        Args:
            data: List of header values for the overview.
            data: List of entries that get written to the file.
            sheet_name (Optional): The name of the worksheet. Defaults to None.
            row_offset: Starting row in the excel workbook. Defaults to 0.
            col_offset: Starting col in the excel workbook. Defaults to 0.

        Raises:
            exceptions.WorkbookError: The active workbook encountered a
                problem. Contains further information about the error.
        """
        workbook = xlsxwriter.Workbook(self.destination)

        # TODO: Maybe use context manager for this
        try:
            tournament_worksheet = workbook.add_worksheet(sheet_name)
        except (
            xlsxwriter.exceptions.InvalidWorksheetName,
            xlsxwriter.exceptions.DuplicateWorksheetName,
        ) as exinfo:
            raise exceptions.WorkbookError from exinfo

        optional_tournament_format = workbook.add_format(
            {"bg_color": "#fcd5b4"}
        )

        # Add the header to the data.
        data = header + data

        for row, obj in enumerate(data):
            for col, datum in enumerate(obj.to_tuple()):
                tournament_worksheet.write_string(
                    row + row_offset,
                    col + col_offset,
                    datum,
                    optional_tournament_format if obj.is_optional else None,
                )

        workbook.close()

