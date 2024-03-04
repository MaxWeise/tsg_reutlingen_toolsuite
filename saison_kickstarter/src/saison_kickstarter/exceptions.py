"""Custom Exceptions Module

This module defines custom exceptions used throughout the application.

Exceptions:
    FileEncodingErro: A file is not in a supported encoding format.

"""

class FileEncodingError(Exception):
    """A file is not in UTF-8 encoding."""
    pass
