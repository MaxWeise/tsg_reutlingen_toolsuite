"""Generate a list of referees.

Created: 30.10.2023
@author: Max Weise
"""

import pathlib
import csv
from typing import Any, Iterator


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


def clean_data(data_table: Any) -> Any:
    """Remove unused data columns from the csv data.

    Args:
        data_table (Any): The data to be cleaned by the function.

    Returns:
        Any: The cleaned data.
    """


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
