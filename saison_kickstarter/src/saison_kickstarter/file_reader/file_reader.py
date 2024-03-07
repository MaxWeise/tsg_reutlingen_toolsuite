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

    @property
    def data_source(self) -> pathlib.Path:
        """The underlying datasource represented as a path."""
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )

    def read_data(self) -> list[tuple[str, str, str, str]]:
        """Read data from a file and return the result.

        Returns:
            A list of tuples. Each tuple represents one line in the csv file.

        Raises:
            FileNotFoundError: The file specified by the path can not be found.
            ValueError: The mime type of the file is not .csv .
            FileEncodingError: The csv file is not in UTF-8 encoding.
        """
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )
