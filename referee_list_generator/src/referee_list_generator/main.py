"""Generate a list of referees.

Created: 30.10.2023
@author: Max Weise
"""

import pathlib
import csv
from typing import Any
from collections.abc import Iterable


class DataTable:
    def __init__(self, header: tuple[str, ...], contents: list[tuple[str, ...]]):
        self._header = header
        self._content = contents

    @property
    def header(self) -> tuple[str, ...]:
        return self._header

    @property
    def content(self) -> list[tuple[str, ...]]:
        return self._content


def read_csv_file(csv_file: pathlib.Path):
    """Read a csv file and retrieve the data.

    Args:
        csv_file (Pathlike): The path to the csv file.

    Returns:
        Any: The contents of the csv file.

    Raises:
        UnicodeDecodeError: When a file is not in UTF-8 encoding.
    """
    with open(csv_file, "r", newline="") as file_contents:
        csv_reader = csv.reader(file_contents, delimiter=";")
        return [tuple(item) for item in csv_reader]


def prepare_data(data_set: Iterable) -> DataTable:
    """Remove unused data columns from the csv data.

    Args:
        data_table (Any): The data to be cleaned by the function.

    Returns:
        Any: The cleaned data.
    """
    data_columns: list[tuple[str, ...]] = [
        (str(row[1]), str(row[2]), str(row[3])) for row in data_set
    ]

    header = tuple(data_columns[0])
    content = data_columns[1 : len(data_columns)]
    return DataTable(header, content)


def write_to_excel_file(data_table: Any) -> Any:
    """Write contents to a formatted excel file.

    Args:
        data_table (Any): The data to be written to the excel file.

    Returns:
        Any: The return value of the function.
    """
    ...


def main():
    """Run the main function of the script."""
    ...


if __name__ == "__main__":
    main()
