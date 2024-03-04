"""Entry point for the application.

Created: 21.02.2024
@author: Max Weise
"""

import argparse
import pathlib
import logging
import logging.config

import saison_kickstarter.controller
import saison_kickstarter.sqlite_adapter
import saison_kickstarter.excel_view_builder
import saison_kickstarter.excel_file_writer


PROJECT_URL: str = r"https://github.com/MaxWeise/tsg_reutlingen_toolsuite"
PROGRAMM_NAME: str = "saison-kickstarter"
EPILOG: str = ("Project created an maintained by Max Weise, 2024. "
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
    "loggers": {
        "root": {"level": "DEBUG", "handlers": ["stdout"]}
    },
}

logging.config.dictConfig(config=logging_config)

logger = logging.getLogger(__name__)


def create_tournament_overview() -> None:
    """Create an overview of all tournaments for the comming saison.

    This function will create objects to handle requirements set by the 
    user.
    """

    data_source = saison_kickstarter.sqlite_adapter.SqliteDatabase(
            "./tournaments.db",
            ""
    )
    view_builder = saison_kickstarter.excel_view_builder.ExcelViewBuilder()
    file_writer = saison_kickstarter.excel_file_writer.ExcelFileWriter()

    try:
        saison_kickstarter.controller.create_tournament_overview(
                pathlib.Path("./turnierübersicht.xlsx"),
                data_source,
                view_builder,
                file_writer,
        )
    except ValueError:
        logger.warning("There are no values present in the database!")



def parse_args() -> argparse.Namespace:
    """Register CLI arguments and return a namespace containing the values."""
    parser = argparse.ArgumentParser(
        prog=PROGRAMM_NAME,
        epilog=EPILOG
    )

    subparsers = parser.add_subparsers(help="Subparsers help")
    create_parser = subparsers.add_parser(
        "create-overview",
        help="Create an overview of a specified dataset.",
    )
    read_parser = subparsers.add_parser(
        "read-data",
        help="Read data from a datasource."
    )

    # Create parser
    domain_choices = ["tournament", "referee"]
    create_parser.add_argument(
        "overview_type",
        metavar="type",
        choices=domain_choices,
        help=("Create an overview of one of the given choices: "
              f"{domain_choices}"
        ),
    )

    # Read parser
    read_parser.add_argument(
        "domain",
        choices=domain_choices,
        help=(
            "Read data entries for one of the following domains: "
            f"{domain_choices}"
        ),
    )

    read_parser.add_argument(
        "-f",
        help="Specify a file to read data from.",
    )

    return parser.parse_args()


def main() -> None:
    """Run the main function."""
    arguments = parse_args()

    if arguments.overview_type == "tournament":
        create_tournament_overview()

if __name__ == "__main__":
    main()
