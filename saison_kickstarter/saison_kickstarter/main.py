"""Entry point for the application.

Created: 21.02.2024
@author: Max Weise
"""

import argparse
import enum
import logging
import logging.config
import pathlib

from saison_kickstarter import (file_reader, file_writer, view_builder,
                                view_item)
from saison_kickstarter.exceptions import FileEncodingError
from saison_kickstarter.file_reader import FileReader
from saison_kickstarter.view_builder import ViewBuilder
from saison_kickstarter.view_item import ViewItem

PROJECT_URL: str = r"https://github.com/MaxWeise/tsg_reutlingen_toolsuite"
PROGRAMM_NAME: str = "saison-kickstarter"
EPILOG: str = (
    "Project created an maintained by Max Weise, 2024. "
    f"Project lives on {PROJECT_URL}"
)


class OverviewType(enum.StrEnum):
    REFEREE = enum.auto()
    TOURNAMENT = enum.auto()

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
        choices=[command.value for command in OverviewType],
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


def create_overview(
        overview: OverviewType,
        data_source: str,
        include_optional: bool,
        out_file_name: pathlib.Path,
) -> None:
    data_file = pathlib.Path(data_source)
    if not data_file.exists():
        raise FileNotFoundError(f"The file {data_file} does not exist!")

    suffix: str = data_file.suffix
    supported_readers: dict[str, FileReader] = {
        ".csv": file_reader.CsvFileReader(data_source),
        ".xlsx": file_reader.ExcelFileReader(data_source),
    }
    reader: FileReader | None = supported_readers.get(suffix)
    if not reader:
        raise ValueError(f"{suffix} is not supported.")

    supported_builders: dict[OverviewType, ViewBuilder] = {
        OverviewType.REFEREE: view_builder.RefereeViewBuilder(),
        OverviewType.TOURNAMENT: view_builder.TournamentViewBuilder(
            include_optional
        ),
    }
    builder: ViewBuilder | None = supported_builders.get(overview)
    if not builder:
        raise ValueError(f"{overview} is not supported in the builder map.")
    writer = file_writer.ExcelFileWriter(out_file_name)

    try:
        data = reader.read_data()
    except FileEncodingError as e:
        raise FileEncodingError(
            f"The file is not in UTF-8 encoding: {data_file}"
        ) from e

    view: list[ViewItem] = list(builder.build_view(data))

    supported_headers: dict[OverviewType, list[ViewItem]] = {
        OverviewType.REFEREE: [
            view_item.HeaderViewItem(
                ["Datum", "Turnier", "Lizenz", "1", "2", "3"]
            )
        ],
        OverviewType.TOURNAMENT: [view_item.HeaderViewItem(["Datum", "Ort"])],
    }
    header = supported_headers.get(overview)
    if not header:
        raise ValueError(f"{overview} is not supported in the builder map.")
    writer.write_overview(header, view)


def main() -> None:
    """Run the main function."""
    arguments = parse_args()
    command = OverviewType(arguments.command)
    out_file_name = pathlib.Path("overview.xlsx")

    try:
        create_overview(
            command,
            arguments.file,
            arguments.inlcude_optional,
            out_file_name
        )
    except (FileNotFoundError, ValueError, FileEncodingError) as e:
        logger.error(e)

    logger.info("Execution finished")


if __name__ == "__main__":
    main()
