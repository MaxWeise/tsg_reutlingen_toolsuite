"""Entry point for the application.

Created: 21.02.2024
@author: Max Weise
"""

import argparse
import enum
import logging
import logging.config
import pathlib

from saison_kickstarter import exceptions
from saison_kickstarter.file_reader import csv_file_reader
from saison_kickstarter.file_reader.file_reader import FileReader
from saison_kickstarter.file_writer import excel_file_writer
from saison_kickstarter.file_writer.file_writer import FileWriter
from saison_kickstarter.view_builder import excel_view_builder
from saison_kickstarter.view_builder.view_builder import ViewBuilder

PROJECT_URL: str = r"https://github.com/MaxWeise/tsg_reutlingen_toolsuite"
PROGRAMM_NAME: str = "saison-kickstarter"
EPILOG: str = (
    "Project created an maintained by Max Weise, 2024. "
    f"Project lives on {PROJECT_URL}"
)


class SupportedCommands(enum.Enum):
    CREATE_TOURNAMENT_OVERVIEW = "create-overview-tournament"


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


def parse_args() -> argparse.Namespace:
    """Register CLI arguments and return a namespace containing the values."""
    parser = argparse.ArgumentParser(prog=PROGRAMM_NAME, epilog=EPILOG)

    parser.add_argument(
        "command",
        choices=[command.value for command in SupportedCommands],
        help="Create an overview from a specified file.",
    )

    parser.add_argument(
        "file",
        help="Specify the file that holds the data for the overview.",
    )

    parser.add_argument(
        "--include-optional",
        action="store_true",
        help="If this flag is set, the overview will include optional tournaments",
    )

    return parser.parse_args()


def main() -> None:
    """Run the main function."""
    arguments = parse_args()

    file_reader: FileReader = csv_file_reader.CsvFileReader(arguments.file)
    view_builder: ViewBuilder = excel_view_builder.TournamentViewBuilder()
    file_writer: FileWriter = excel_file_writer.ExcelFileWriter()

    if arguments.command == SupportedCommands.CREATE_TOURNAMENT_OVERVIEW.value:
        data = file_reader.read_data()
        view_builder.build_view(data, arguments.include_optional)


if __name__ == "__main__":
    main()
