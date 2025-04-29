"""A module for reading data from CSV files.

This module provides a CsvFileReader class that allows users to read data
from CSV files and retrieve their contents.

@author: Max Weise
"""

import csv
import pathlib

from saison_kickstarter import exceptions, tournament


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
