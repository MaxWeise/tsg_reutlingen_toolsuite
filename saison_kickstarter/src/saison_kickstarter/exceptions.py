"""Custom Exceptions Module

This module defines custom exceptions used throughout the application.

Exceptions:
    FileEncodingErro: A file is not in a supported encoding format.

"""


class FileEncodingError(Exception):
    """A file is not in UTF-8 encoding."""


class FileReadError(Exception):
    """An error occured while trying to read a file."""


class DatabaseWriteError(Exception):
    """An error occured while trying to write to a database."""
