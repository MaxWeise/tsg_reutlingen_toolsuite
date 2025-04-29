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

    @property
    def data_source(self) -> pathlib.Path:
        """The file the data is read from."""
        return self._data_source

    def _construct_dict_from_tuple(
        self, data: tuple[str, str, str, str]
    ) -> dict[str, str]:
        """Take a tuple and construct a dictionary from the given values.

        Args:
            data: The tuple containing data.

        Returns:
            A dictionary containing values.
        """
        date, city, category, age_group = data
        ret = {}
        # Parse the dates into two parts
        if len(date) < 14:
            raise ValueError(
                f"Wrong date-format recieved: {date}."
                "\nDate should follow either"
                " dd./dd.mm.yyyy or dd.mm./dd.mm.yyyy format!"
            )

        parts_uncleaned = date.split(".")
        parts = [part.replace("/", "") for part in parts_uncleaned]

        if len(date) == 14:
            # Handle Weekend in same month
            first_day, second_day, month, year = parts
            ret["first_day"] = f"{first_day}.{month}.{year}"
            ret["second_day"] = f"{second_day}.{month}.{year}"
        else:
            first_day, first_month, second_day, second_month, year = parts
            ret["first_day"] = f"{first_day}.{first_month}.{year}"
            ret["second_day"] = f"{second_day}.{second_month}.{year}"

        ret["city"] = city
        ret["category"] = category
        ret["age_group"] = age_group

        return ret

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

                # Create dictionaries from tuple data
                dict_data: list[dict[str, str]] = [
                    self._construct_dict_from_tuple(item) for item in data  # type: ignore
                ]

                ret = [tournament.tournament_from_dict(t) for t in dict_data]

                return ret
        except UnicodeDecodeError as exc:
            raise exceptions.FileEncodingError(
                f"The file is not in UTF-8 encoding: {self._data_source}"
            ) from exc
