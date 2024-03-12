"""Entry point for the application.

Created: 21.02.2024
@author: Max Weise
"""

import argparse
import logging
import logging.config
import pathlib

from saison_kickstarter import controller, exceptions
from saison_kickstarter.database import sqlite_adapter
from saison_kickstarter.file_reader import csv_file_reader
from saison_kickstarter.file_writer import excel_file_writer
from saison_kickstarter.view_builder import excel_view_builder

PROJECT_URL: str = r"https://github.com/MaxWeise/tsg_reutlingen_toolsuite"
PROGRAMM_NAME: str = "saison-kickstarter"
EPILOG: str = (
    "Project created an maintained by Max Weise, 2024. "
    f"Project lives on {PROJECT_URL}"
)

# Logging config goes here
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(levelname)s |  func::%(funcName)s] %(message)s",
        },
        "console": {
            "format": "[%(levelname)s] %(message)s",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "console",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {"root": {"level": "DEBUG", "handlers": ["stdout"]}},
}

logging.config.dictConfig(config=logging_config)

logger = logging.getLogger(__name__)


def read_data_from_file(data_file: str) -> None:

    reader = csv_file_reader.CsvFileReader(data_file)
    data_source = sqlite_adapter.SqliteDatabase("./tournaments.db", "")

    try:
        controller.read_tournaments_from_file(reader, data_source)
    except exceptions.FileReadError as ex:
        logger.error(f"Something went wrong while reading from a file: {ex}")


def create_tournament_overview() -> None:
    """Create an overview of all tournaments for the comming saison.

    This function will create objects to handle requirements set by the
    user.
    """

    data_source = sqlite_adapter.SqliteDatabase("./tournaments.db", "")
    view_builder = excel_view_builder.ExcelViewBuilder()
    file_writer = excel_file_writer.ExcelFileWriter()

    try:
        controller.create_tournament_overview(
            pathlib.Path("./turnierübersicht.xlsx"),
            data_source,
            view_builder,
            file_writer,
        )
    except ValueError:
        logger.warning("There are no values present in the database!")


def parse_args() -> argparse.Namespace:
    """Register CLI arguments and return a namespace containing the values."""
    parser = argparse.ArgumentParser(prog=PROGRAMM_NAME, epilog=EPILOG)
    available_commands = ["create-overview", "read-data"]
    # domain_choices = ["tournament", "referee"]

    parser.add_argument(
        "command",
        choices=available_commands,
        help="Use stored data to create an overview of the given doamin.",
    )

    return parser.parse_args()


def main() -> None:
    """Run the main function."""
    arguments = parse_args()
    print(arguments)


if __name__ == "__main__":
    main()
