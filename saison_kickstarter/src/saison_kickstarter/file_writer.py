"""Define a protocol that handles interactions with files.

Created: 03.02.2024
@author: Max Weise
"""

import pathlib
import typing

from saison_kickstarter.view_builder import OverviewEntry


class FileWriter(typing.Protocol):
    """Define methods to write to a file."""

    def write_tournament_overview(
        self,
        file: pathlib.Path,
        tournaments: list[OverviewEntry],
        row: int = 0,
        col: int = 0,
    ) -> None:
        """Write a given contents to a file of specified mime-type.

        Args:
            file: The name of the file that is created.
            contents: A list of entries, that will be written in the file.
        """
        raise NotImplementedError()
