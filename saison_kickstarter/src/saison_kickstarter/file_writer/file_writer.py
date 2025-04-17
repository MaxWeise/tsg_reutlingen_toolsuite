"""An interface to write data to files.

The file-writer interface encapsules common attributes and operations
to handle a datasource and writing data to it.


Created: 11.04.2025
@author: Max Weise
"""

import pathlib
from typing import Protocol


class FileWriter(Protocol):
    """Write content to files.

    Attributes:
        data_source: The path to the file.
    """

    def write_data(self, file_: pathlib.Path, data: list[tuple]) -> None:
        """Write data to a file."""
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )
