"""Define classes that can be used in tests to mock the behaviour of components.
Created: 18.02.2024
@author: Max Weise
"""

import pathlib
from datetime import date
from typing import Any

from typing_extensions import override

from saison_kickstarter.database.database_item import DatabaseItem
from saison_kickstarter.file_writer.excel_file_writer import ExcelFileWriter
from saison_kickstarter.tournament import Tournament
from saison_kickstarter.view_builder.view_builder import OverviewEntry


class MockDatabase:
    """Implement the database interface as a mock"""

    def __init__(self, *, is_empty: bool = False) -> None:
        self.is_empty = is_empty

    def create(self, item: DatabaseItem) -> bool | None:
        """Create a resouce in the underlying table."""
        _ = item
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )

    def read(self) -> list[Any] | None:
        """Read all values from a database table."""
        if self.is_empty:
            return []

        return [
            (1, date(2000, 4, 13), "Reutlingen", "RL", "U15"),
            (2, date(2000, 5, 31), "Osnabrück", "RL", "U17"),
            (3, date(2000, 2, 2), "Ditzigen", "RL", "U13"),
            (4, date(2000, 3, 15), "Heidenheim", "RL", "U15"),
            (5, date(2000, 11, 25), "Reutlingen", "QB", "Senioren"),
            (6, date(2000, 1, 1), "Reutlingen", "RL", "U15"),
        ]


class MockViewBuilder:
    """Implement the view-builder interface as a mock"""

    def build_tournament_overview(
        self, data: list[Tournament]
    ) -> list[OverviewEntry]:
        _ = data
        return [
            # U13 Turniere
            ("02.02.2000", "RL-U13 Ditzigen", False),
            ("01.01.2000", "RL-U15 Reutlingen", True),
            ("15.03.2000", "RL-U15 Heidenheim", True),
            ("13.04.2000", "RL-U15 Reutlingen", True),
            # U15 Turniere
            ("01.01.2000", "RL-U15 Reutlingen", False),
            ("15.03.2000", "RL-U15 Heidenheim", False),
            ("13.04.2000", "RL-U15 Reutlingen", False),
            ("31.05.2000", "RL-U17 Osnabrück", True),
            # U17 Turniere
            ("31.05.2000", "RL-U17 Osnabrück", False),
            # Senioren Tourniere
            ("25.11.2000", "QB Reutlingen", False),
        ]


class MockFileWriter(ExcelFileWriter):

    @override
    def write_tournament_overview(
        self,
        file: pathlib.Path,
        tournaments: list[OverviewEntry],
        row: int = 0,
        col: int = 0,
    ) -> None: ...
