"""A module for reading data from Excel files.

This module provides a ExcelFileReader class that allows users to read data
from Excel tables and retrieve their contents.

Created: 28.04.2025
@author: Max Weise
"""

import pathlib

import pandas as pd

from saison_kickstarter import tournament


class ExcelFileReader:
    """A file reader that reads tournament data from an excel file.

    Attributes:
        _file_path (pathlib.Path): The path to the excel file.
    """

    def __init__(self, file_path: str) -> None:
        self._file_path = pathlib.Path(file_path)

    def read_data(self) -> list[tournament.Tournament]:
        """Read data from an excel file and return the result.

        Returns:
            A list of tuples. Each tuple represents one line in the csv file.

        Raises:
            FileNotFoundError: The file can not be found.
            ValueError: The mime type of the file is not correct .
        """

        if not self._file_path.exists():
            raise FileNotFoundError(
                f"The file does not exist: {self._file_path}"
            )

        if self._file_path.suffix != ".xlsx":
            raise ValueError(
                f"File extention is not supported: {self._file_path}"
            )

        df = pd.read_excel(self._file_path)

        data = []
        for row in df.itertuples():
            data.append(
                (
                    row.Datum,  # type: ignore
                    row.Ort,  # type: ignore
                    row.Kategorie,  # type: ignore
                    row.Altersklasse,  # type: ignore
                )
            )

        return [tournament.tournament_from_tuple(row) for row in data]
