"""An interface to write data to files.

The file-writer interface encapsules common attributes and operations
to handle a datasource and writing data to it.


Created: 11.04.2025
@author: Max Weise
"""

from typing import Protocol

from saison_kickstarter import view_item


class FileWriter(Protocol):
    """Write content to files."""

    def write_tournament_data(
        self, data: list[view_item.ViewItem], row: int = 0, col: int = 0
    ) -> None:
        """Write data to a file."""
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )

    def write_referee_data(
        self, data: list[view_item.RefereeViewItem], row: int = 0, col: int = 0
    ) -> None:
        """Write data to a file."""
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )
