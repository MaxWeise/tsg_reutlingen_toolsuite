"""Entry point for the application.

Created: 21.02.2024
@author: Max Weise
"""

import argparse
import enum
import logging
import logging.config
import pathlib

from saison_kickstarter import file_reader, file_writer, view_builder
from saison_kickstarter.exceptions import FileEncodingError, WorkbookError

PROJECT_URL: str = r"https://github.com/MaxWeise/tsg_reutlingen_toolsuite"
PROGRAMM_NAME: str = "saison-kickstarter"
EPILOG: str = (
    "Project created an maintained by Max Weise, 2024. "
    f"Project lives on {PROJECT_URL}"
)

OUT_EXCEL_FILE: pathlib.Path = pathlib.Path("./overview-file.xlsx")


class SupportedCommands(enum.Enum):
    CREATE_TOURNAMENT_OVERVIEW = "create-overview-tournament"
    CREATE_REFEREE_OVERVIEW = "create-overview-referee"


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
        help=(
            "If this flag is set,"
            " the overview will include optional tournaments"
        ),
    )

    return parser.parse_args()


def _create_tournament_overview(data_file: str, out_file: pathlib.Path, include_optional: bool = False) -> None:
    """Define the workflow to create an overview over all tournaments."""
    suffix = pathlib.Path(data_file).suffix

    reader = file_reader.ExcelFileReader(data_file) if suffix == ".xlsx" else file_reader.CsvFileReader(data_file)
    builder = view_builder.TournamentViewBuilder(include_optional)
    writer = file_writer.ExcelFileWriter(out_file)

    try:
        tournaments = reader.read_data()
    except (FileNotFoundError, ValueError, FileEncodingError) as e:
        logger.error("An exception occured while reading the given file: %s", e)
        return

    view = builder.build_view(tournaments)

    try:
        writer.write_tournament_data(view)
    except WorkbookError as e:
        logger.error("An exception occured while writing data to the excel file: %s", e)
        return


def _create_referee_overview(data_file: str, out_file: pathlib.Path) -> None:
    """Define the workflow to create an overview over all needed referees."""
    suffix = pathlib.Path(data_file).suffix

    reader = file_reader.ExcelFileReader(data_file) if suffix == ".xlsx" else file_reader.CsvFileReader(data_file)
    builder = view_builder.RefereeViewBuilder()
    writer = file_writer.ExcelFileWriter(out_file)

    try:
        tournaments = reader.read_data()
    except (FileNotFoundError, ValueError, FileEncodingError) as e:
        logger.error("An exception occured while reading the given file: %s", e)
        return

    view = builder.build_view(tournaments)

    try:
        writer.write_referee_data(view)
    except WorkbookError as e:
        logger.error("An exception occured while writing data to the excel file: %s", e)
        return

def main() -> None:
    """Run the main function."""
    arguments = parse_args()
    command = SupportedCommands(arguments.command)

    if command == SupportedCommands.CREATE_TOURNAMENT_OVERVIEW:
        logger.info(f"Selected command: {command}")
        _create_tournament_overview(
            arguments.file,
            pathlib.Path("turnierübersicht.xlsx"),
            arguments.include_optional
        )

    if command == SupportedCommands.CREATE_REFEREE_OVERVIEW:
        logger.info(f"Selected command: {command}")
        _create_referee_overview(
            arguments.file,
            pathlib.Path("kampfrichterübersicht.xlsx"),
        )

    logger.info("Execution finished")


if __name__ == "__main__":
    main()
