"""Entry point for the application.

Created: 21.02.2024
@author: Max Weise
"""

import argparse
import enum
import logging
import logging.config
import pathlib

from saison_kickstarter.exceptions import FileEncodingError, WorkbookError
from saison_kickstarter.reader import csv_file_reader
from saison_kickstarter.reader.file_reader import FileReader
from saison_kickstarter.view_builder import excel_view_builder
from saison_kickstarter.view_builder.view_builder import ViewBuilder
from saison_kickstarter.writer import excel_file_writer
from saison_kickstarter.writer.file_writer import FileWriter

PROJECT_URL: str = r"https://github.com/MaxWeise/tsg_reutlingen_toolsuite"
PROGRAMM_NAME: str = "saison-kickstarter"
EPILOG: str = (
    "Project created an maintained by Max Weise, 2024. "
    f"Project lives on {PROJECT_URL}"
)

EXCEL_FILE: pathlib.Path = pathlib.Path("./tournament-overview-file.xlsx")


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


def main(command: str, csv_file: str, include_optional: bool = False) -> None:
    """Run the main function."""

    file_reader: FileReader = csv_file_reader.CsvFileReader(csv_file)
    view_builder: ViewBuilder = excel_view_builder.ExcelViewBuilder()
    file_writer: FileWriter = excel_file_writer.ExcelFileWriter(EXCEL_FILE)

    if command == SupportedCommands.CREATE_TOURNAMENT_OVERVIEW.value:
        try:
            data = file_reader.read_data()
        except FileNotFoundError:
            logger.error(f"File does not exist: {csv_file}")
            return
        except ValueError:
            logger.error(f"This file type is unsuported: {csv_file}")
            return
        except FileEncodingError:
            logger.error(f"This file has the wrong encoding: {csv_file}")
            return

        view_data = view_builder.build_view(data, include_optional)

        try:
            file_writer.write_data(view_data)
        except WorkbookError as e:
            logger.error(f"There has been an error with the workbook: {e}")
            return


if __name__ == "__main__":
    arguments = parse_args()
    main(arguments.command, arguments.file, arguments.include_optional)
