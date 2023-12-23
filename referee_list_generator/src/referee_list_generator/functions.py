"""Functions that define the steps of the script.

Created: 23.12.2023
@author: Max Weise
"""

import csv
import pathlib
import typing

import xlsxwriter  # type: ignore

from referee_list_generator import system_core


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


def get_data_rows(data: list[tuple[str, ...]]) -> list[system_core.DataRow] | None:
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
    data_rows: list[system_core.DataRow] = []

    # remove headings from data
    data_without_headings = data[1:]

    for row in data_without_headings:
        last_name = row[1]
        first_name = row[2]
        year_of_birth = _get_year_of_birth(row[3])

        if not year_of_birth:
            continue

        current_element = system_core.DataRow(last_name, first_name, year_of_birth)
        data_rows.append(current_element)

    return data_rows


def _write_headers(worksheet: typing.Any, offset: int):
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
        raise system_core.ExcelWriteError(str(e))


def _write_data(worksheet: typing.Any, data: list[system_core.DataRow], offset: int):
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
        raise system_core.ExcelWriteError(str(e))


def write_data_to_excel_file(
    data: list[system_core.DataRow], excel_file: pathlib.Path
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
    except system_core.ExcelWriteError as e:
        workbook.close()
        return None
    finally:
        workbook.close()

    return True
