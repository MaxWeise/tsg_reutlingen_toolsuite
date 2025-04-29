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

    def _get_two_dates_from_string(self, date: str) -> tuple[str, str]:
        """Parse the date from a combined view to two seperate dates.

        Normally the input will be in a dd./dd.mm.yyyy or in a dd.mm/dd.mm.yyyy
        format. This needs to be parsed to two seperate entrys for the
        tournament object.

        Args:
            date (str): The date in the combined dd./dd.mm.yyyy or
                dd.mm/dd.mm.yyyy format.

        Returns:
            A tuple containing the two date entrys.

        Raises:
            ValueError: The date is in the wrong format.
        """

        if len(date) < 14:
            raise ValueError(
                f"Wrong date-format recieved: {date}."
                "\nDate should follow either dd./dd.mm.yyyy or dd.mm./dd.mm.yyyy format!"
            )

        parts_uncleaned = date.split(".")
        parts = [part.replace("/", "") for part in parts_uncleaned]

        if len(date) == 14:
            # Handle Weekend in same month
            first_day, second_day, month, year = parts

            return (
                f"{first_day}.{month}.{year}",
                f"{second_day}.{month}.{year}",
            )
        else:
            first_day, first_month, second_day, second_month, year = parts
            return (
                f"{first_day}.{first_month}.{year}",
                f"{second_day}.{second_month}.{year}",
            )

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

        ret = []
        for row in df.itertuples(index=False):
            # Names are in german, as the input file will be in german
            dates = self._get_two_dates_from_string(row.Datum)  # type: ignore
            fd = tournament.date_from_string(dates[0])
            sd = tournament.date_from_string(dates[1])

            cat = tournament.category_from_string(row.Kategorie)  # type: ignore
            age = tournament.age_group_from_string(
                row.Altersklasse  # type: ignore
            )

            t = tournament.Tournament(
                first_day=fd,
                second_day=sd,
                city=row.Ort,  # type: ignore
                category=cat,
                age_group=age,
            )
            ret.append(t)

        return ret
