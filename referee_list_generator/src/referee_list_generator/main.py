"""Generate a list of referees.

Created: 30.10.2023
@author: Max Weise
"""

import csv
import dataclasses
import pathlib
from typing import Any

import xlsxwriter  # type: ignore


@dataclasses.dataclass
class ExcelWriteError(Exception):
    """When an exception is raised while trying to write to an excel file.

    Args:
        message (str): The message raised by the previous exception.
    """

    message: str


@dataclasses.dataclass
class DataRow:
    """A row in a spreadsheet holding information about a referee.

    Attributes:
        last_name: The last name of the person. Used as primary key.
        first_name: The filst name of the person.
        year_of_birth: The year in which the person was born.
        training_D_licence: Wheather or not the person has completet
            the training for the regional D-licence.
        obtained_D_licence: Wheather or not the person has obtained the
            regional refereeing-licence.
        training_CN_licence: Wheather or not the person has completet
            the training for the national CN-licence.
        obtained_CN_licence: Wheather or not the person has obtained the
            national refereeing-licence.
    """

    last_name: str
    first_name: str
    year_of_birth: str
    training_D_licence: bool = False
    _obtained_D_licence: bool = False
    _expiration_date_d_licence: str | None = None
    _training_CN_licence: bool = False
    _obtained_CN_licence: bool = False

    @property
    def begun_training_D_licence(self) -> str:
        """Map the property to a human readable string."""
        return "Ja" if self.training_D_licence else "Nein"

    @property
    def obtained_D_licence(self) -> str:
        """Map the property to a human readable string."""
        return "Ja" if self._obtained_D_licence else "Nein"

    @property
    def expiration_date_d_licence(self) -> str:
        """Map the property to a human readable string."""
        return (
            "---"
            if self._expiration_date_d_licence is None
            else str(self._expiration_date_d_licence)
        )

    @property
    def training_CN_licence(self) -> str:
        """Map the property to a human readable string."""
        return "Ja" if self._training_CN_licence else "Nein"

    @property
    def obtained_CN_licence(self) -> str:
        """Map the property to a human readable string."""
        return "Ja" if self._obtained_CN_licence else "Nein"


class Maybe:
    """Monad-like class that handles errors through none values.

    Attributes:
        _value (T): The value of the monad type.
    """

    def __init__(self, value):
        """Initialize a Maybe instance.

        Args:
            value (T): The value of the maybe-instance.
        """
        self._value = value

    @property
    def value(self):
        """The value of the monad."""
        return self._value

    def bind(self, func):
        """Apply a function to the internal value.

        In case of errors or missing values, a function should return no value.
        The Maybe monad propagates the error / missing value thorughout the
        programm.

        Args:
            func (T -> U | None): A function that takes a value and returns
                a new value or none.

        Returns:
            result (Maybe<T | None>): A monad object that holds the result of
                the computation done by func.
        """
        if self._value is None:
            return Maybe(None)

        result = func(self._value)
        return Maybe(result)


def read_csv_file(csv_file: pathlib.Path) -> list[tuple[str, ...]] | None:
    """Read a csv file and retrieve the data.

    Args:
        csv_file (Pathlike): The path to the csv file.

    Returns:
        Any: The contents of the csv file.

    Raises:
        UnicodeDecodeError: When a file is not in UTF-8 encoding.
    """
    if not csv_file.exists():
        return None

    try:
        with open(csv_file, "r", newline="") as file_contents:
            csv_reader = csv.reader(file_contents, delimiter=";")
            return [tuple(item) for item in csv_reader]
    except UnicodeDecodeError:
        return None


def _get_year_of_birth(date: str | None) -> str | None:
    if not date:
        return None

    return date.split(".")[-1]


def get_data_rows(data: list[tuple[str, ...]]) -> list[DataRow] | None:
    """Populate a list with data objects, that hold personal information.

    Construct objects from individual rows of a csv-file. The function
    returns only the values from the tuply specified by the DataRow class.
    In the process of selecting the needed data, the table-headings will be
    removed, so the firt element of the return value contains actual
    information instead of headings.

    Args:
        data: Data organized as a list of tuples.

    Returns:
        A list of objects that hold specified data to be evaluated at a later
        point in time.
    """
    data_rows: list[DataRow] = []

    # remove headings from data
    data_without_headings = data[1:]

    for row in data_without_headings:
        last_name = row[1]
        first_name = row[2]
        year_of_birth = _get_year_of_birth(row[3])

        if not year_of_birth:
            continue

        current_element = DataRow(last_name, first_name, year_of_birth)
        data_rows.append(current_element)

    return data_rows


def _write_headers(worksheet: Any, offset: int):
    try:
        worksheet.write(f"C{offset - 1}", "Name")
        worksheet.write(f"D{offset - 1}", "Vorname")
        worksheet.write(f"E{offset - 1}", "Jahrgang")
        worksheet.write(f"F{offset - 1}", "Lehrgang D-Lizenz")
        worksheet.write(f"G{offset - 1}", "D-Lizenz")
        worksheet.write(f"H{offset - 1}", "Ablaufdatum D-Lizenz")
        worksheet.write(f"I{offset - 1}", "Lehrgang CN-Lizenz")
        worksheet.write(f"J{offset - 1}", "CN-Lizenz")
    except Exception as e:
        raise ExcelWriteError(str(e))


def _write_data(worksheet: Any, data: list[DataRow], offset: int):
    try:
        for position, value in enumerate(data):
            worksheet.write(f"C{position + offset}", value.last_name)
            worksheet.write(f"D{position + offset}", value.first_name)
            worksheet.write(f"E{position + offset}", value.year_of_birth)
            worksheet.write(f"F{position + offset}", value.begun_training_D_licence)
            worksheet.write(f"G{position + offset}", value.obtained_D_licence)
            worksheet.write(f"H{position + offset}", value.expiration_date_d_licence)
            worksheet.write(f"I{position + offset}", value.training_CN_licence)
            worksheet.write(f"J{position + offset}", value.obtained_CN_licence)
    except Exception as e:
        raise ExcelWriteError(str(e))


def write_data_to_excel_file(
    data: list[DataRow], excel_file: pathlib.Path
) -> bool | None:
    """Write given data to an excel file.

    Args:
        excel_file: The path to the excel file.
        data: A list of data objects holding the data that should be written
            to the file.

    Returns:
        True if no errors occured during the execution of the function.
        False otherwise.
    """
    workbook = xlsxwriter.Workbook(excel_file)
    worksheet = workbook.add_worksheet(name="Referees")
    offset = 5

    try:
        _write_headers(worksheet, offset)
        _write_data(worksheet, data, offset)
    except Exception as e:
        # TODO: Don't catch all the exceptions, see the docs for the actual
        print(f"This exception occured while writing data to the excel file: {e}")
        workbook.close()
        return None
    finally:
        workbook.close()

    return True


def main():
    """Run the main function of the script."""
    ...


if __name__ == "__main__":
    main()
