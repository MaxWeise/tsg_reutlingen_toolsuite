"""An interface to read data from files.

The file-reader interface encapsules common attributes and operations
to handle a datasource and reading data from it.

Created: 28.02.2024
@author: Max Weise
"""

import typing

from saison_kickstarter import tournament


class FileReader(typing.Protocol):
    """The interface to interact with files."""

    def read_data(self) -> list[tournament.Tournament]:
        """Read data from a file and return the result.

        Returns:
            A list of tuples. Each tuple represents one line in the csv file.

        Raises:
            FileNotFoundError: The file can not be found.
            ValueError: The mime type of the file is not correct .
            FileEncodingError: The file is not UTF-8 encoded.
        """
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )
