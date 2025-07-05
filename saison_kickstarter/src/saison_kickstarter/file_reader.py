"""Define classes that read data from files.

The file-reader interface encapsules common attributes and operations
to handle a datasource and reading data from it.

Created: 05.07.2025
@author: Max Weise
"""

import csv
import pathlib
import typing

import pandas as pd

from saison_kickstarter import exceptions, tournament


class FileReader(typing.Protocol):
    """The interface to interact with files."""

    def read_data(self) -> list[tournament.Tournament]:
        """Read data from a file and return the result.

        Returns:
            A list of tuples. Each tuple represents one line in the csv file.

        Raises:
            FileNotFoundError: The file can not be found.
            ValueError: The mime type of the file is not correct .
            FileEncodingError: The file is not UTF-8 encoded.
        """
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )


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


class CsvFileReader:
    """Provide in interface to interact with csv files.

    Attributes:
        data_source: The Path to an underlying csv file.
    """

    def __init__(self, data_source: str) -> None:
        self._data_source = pathlib.Path(data_source)

    def read_data(self) -> list[tournament.Tournament]:
        """Read data from a file and return the result.

        Returns:
            A list of tournaments, as specified in the csv file.

        Raises:
            FileNotFoundError: The file specified by the path can not be found.
            ValueError: The mime type of the file is not .csv .
            FileEncodingError: The csv file is not in UTF-8 encoding.
        """

        if not self._data_source.exists():
            raise FileNotFoundError(
                f"The file {self._data_source} does not exist!"
            )

        file_suffix: str = self._data_source.suffix
        if file_suffix != ".csv":
            raise ValueError(f"Wrong mime type: {file_suffix}")

        try:
            with open(
                self._data_source, "r", newline="", encoding="utf-8"
            ) as file_contents:
                csv_reader = csv.reader(
                    file_contents, delimiter=",", skipinitialspace=True
                )
                data = [tuple(item) for item in csv_reader if tuple(item)]
                data.pop(0)  # Remove csv header from data

                if len(data[0]) != 4:
                    raise TypeError("Tuple needs to be of length 4")

                return [
                    tournament.tournament_from_tuple(t)  # type: ignore
                    for t in data
                ]
        except UnicodeDecodeError as exc:
            raise exceptions.FileEncodingError(
                f"The file is not in UTF-8 encoding: {self._data_source}"
            ) from exc
