"""Generate a list of referees.

Created: 30.10.2023
@author: Max Weise
"""

import argparse
from typing import Any


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


def main():
    """Run the main function of the script."""
    cli_arguments = setup_cli_arguments()


if __name__ == "__main__":
    main()
