"""Generate a list of referees.

Created: 30.10.2023
@author: Max Weise
"""

import argparse
import pathlib
from typing import Any

from referee_list_generator import functions, system_core


def setup_cli_arguments() -> Any:
    """Define the cli-arguments for the script.

    Returns:
        A Namespace object that contains values of the cli arguments.
    """
    parser = argparse.ArgumentParser(
        prog="KaRi-Listen Generator",
        description="Erstelle eine formattierte Excelliste aus den Einträgen einer CSV Datei.",
    )

    parser.add_argument("filename", help="Pfad zur CSV-Datei", type=str)

    return parser.parse_args()


def main():
    """Run the main function of the script."""
    cli_arguments = setup_cli_arguments()
    file_name = pathlib.Path(cli_arguments.filename)
    csv_file = system_core.Maybe(file_name)
    csv_data = csv_file.bind(functions.read_csv_file)
    data_rows = csv_data.bind(functions.get_data_rows)
    success = data_rows.bind(functions.write_data_to_excel_file)

    print(f"Programm has succeeded: {True if success.value else False}")


if __name__ == "__main__":
    main()
