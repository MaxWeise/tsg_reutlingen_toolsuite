"""A module for reading data from CSV files.

This module provides a CsvFileReader class that allows users to read data
from CSV files and retrieve their contents.

Classes:
    CsvFileReader: A class for reading data from CSV files.

Example:
    To use CsvFileReader to read data from a CSV file:

    >>> reader = CsvFileReader('example.csv')
    >>> data = reader.read_data()
    >>> print(data)
    [('Name', 'Age', 'City'),
     ('John Doe', '30', 'New York'),
     ('Jane Smith', '25', 'Los Angeles')]

Note:
    The CsvFileReader class assumes that the CSV file
        has a header row with column names.

Attributes:
    data_source (Path): The path to the CSV file.

Methods:
    read_data(): Read data from the CSV file and return a list of
        tuples representing the contents.

Usage:
    >>> reader = CsvFileReader('example.csv')
    >>> data = reader.read()
"""

import csv
import pathlib
import typing

from saison_kickstarter.exceptions import FileEncodingError


class CsvFileReader:
    """Provide in interface to interact with csv files.

    Attributes:
        data_source: The Path to an underlying csv file.
    """

    def __init__(self, data_source: str) -> None:
        self._data_source = pathlib.Path(data_source)

    @property
    def data_source(self) -> pathlib.Path:
        """The file the data is read from."""
        return self._data_source

    def _clean_data(
        self, data: list[tuple[str, str, str, str]]
    ) -> list[tuple[str, str, str, str]]:
        """Bring the given data in a presentable format.

        Remove unnecessary whitespace and newlines from the data.
        Remove the header line from the data.

        Returns:
            List of tuples without header line and additional white space.
        """
        data.pop(0)
        for row in data:
            for element in row:
                element.strip()

        return data

    def read_data(self) -> list[tuple[str, str, str, str]]:
        """Read data from a file and return the result.

        Returns:
            A list of tuples. Each tuple represents one line in the csv file.

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
            print(f"This is the mime type: {file_suffix = }")
            raise ValueError(f"Wrong mime type: {file_suffix}")

        try:
            with open(
                self._data_source, "r", newline="", encoding="utf-8"
            ) as file_contents:
                csv_reader = csv.reader(
                    file_contents, delimiter=",", skipinitialspace=True
                )
                data = [tuple(item) for item in csv_reader]
                data.pop(0)

                # Explicit type cast to silence lsp warning
                return typing.cast(list[tuple[str, str, str, str]], data)
        except UnicodeDecodeError as exc:
            raise FileEncodingError(
                f"The file is not in UTF-8 encoding: {self._data_source}"
            ) from exc
