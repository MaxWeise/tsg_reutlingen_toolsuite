"""A module for reading data from Excel files.

This module provides a ExcelFileReader class that allows users to read data
from Excel tables and retrieve their contents.

Created: 28.04.2025
@author: Max Weise
"""

import pandas as pd

from saison_kickstarter import tournament


class ExcelFileReader:

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def _get_two_dates_from_string(self, date: str) -> dict[str, str]:
        if len(date) < 14:
            raise ValueError(
                f"Wrong date-format recieved: {date}."
                "\nDate should follow either dd./dd.mm.yyyy or dd.mm./dd.mm.yyyy format!"
            )

        parts_uncleaned = date.split(".")
        parts = [part.replace("/", "") for part in parts_uncleaned]

        ret = {}
        if len(date) == 14:
            # Handle Weekend in same month
            first_day, second_day, month, year = parts
            ret["first_day"] = f"{first_day}.{month}.{year}"
            ret["second_day"] = f"{second_day}.{month}.{year}"
        else:
            first_day, first_month, second_day, second_month, year = parts
            ret["first_day"] = f"{first_day}.{first_month}.{year}"
            ret["second_day"] = f"{second_day}.{second_month}.{year}"

        return ret

    def read_data(self) -> list[tournament.Tournament]:
        """Read data from an excel file and return the result.

        Returns:
            A list of tuples. Each tuple represents one line in the csv file.

        Raises:
            FileNotFoundError: The file can not be found.
            ValueError: The mime type of the file is not correct .
            FileEncodingError: The file is not UTF-8 encoded.
        """
        df = pd.read_excel(self._file_path)

        ret = []
        for row in df.itertuples(index=False):
            # Names are in german, as the input file will be in german
            dates = self._get_two_dates_from_string(row.Datum)  # type: ignore
            fd = tournament.date_from_string(dates["first_day"])
            sd = tournament.date_from_string(dates["second_day"])

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
