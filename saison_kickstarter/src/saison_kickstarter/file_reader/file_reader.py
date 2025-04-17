"""An interface to read data from files.

The file-reader interface encapsules common attributes and operations
to handle a datasource and reading data from it.

Common usage:
    data_file = Path("./path/to/file.mime")
    file_rader: FileRader = SpecificFileReader(data_file)

    data = file_rader.read_data()

    # Handle data further

Created: 28.02.2024
@author: Max Weise
"""

import pathlib
import typing


class FileReader(typing.Protocol):
    """The interface to interact with files."""

    def read_data(self) -> list[dict[str, str]]:
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
