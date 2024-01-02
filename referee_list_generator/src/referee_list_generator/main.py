"""Generate a list of referees.

Created: 30.10.2023
@author: Max Weise
"""

import argparse
import functools
import pathlib
from typing import Any

from referee_list_generator import functions, system_core

# Metadata
PROGRAMM_NAME = "KaRi-Listen Generator"
DESCRIPTION = (
    "Erstelle eine formattierte Excelliste aus den "
    "Einträgen einer CSV Datei."
)

EXCEL_FILE = pathlib.Path("./output_file.xlsx")


def setup_cli_arguments() -> argparse.Namespace:
    """Define the cli-arguments for the script.

    Returns:
        A Namespace object that contains values of the cli arguments.
    """
    parser = argparse.ArgumentParser(
        prog=PROGRAMM_NAME,
        description=DESCRIPTION,
    )

    parser.add_argument("filename", help="Pfad zur CSV-Datei", type=str)

    return parser.parse_args()


def main(
    csv_filename: str | None = None, excel_file: pathlib.Path = EXCEL_FILE
) -> Any:
    """Run the main function of the script."""
    if not csv_filename:
        raise system_core.MissingArgumentError(
            "The argument: filename is missing. "
            "Please specify a UTF-8 csv file."
        )

    write_to_excel_file = functools.partial(
        functions.write_data_to_excel_file, excel_file=excel_file
    )
    file_name = pathlib.Path(csv_filename)
    csv_file = system_core.Maybe(file_name)
    csv_data = csv_file.bind(functions.read_csv_file)
    data_rows = csv_data.bind(functions.get_data_rows)
    result = data_rows.bind(write_to_excel_file)

    return result.value


if __name__ == "__main__":
    cli_arguments = setup_cli_arguments()
    success = main(cli_arguments.filename)
    print(f"Programm has succeeded: {True if success else False}")
