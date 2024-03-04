"""Define the structure of an Item that can be stored in a database.

Created: 20.01.2024
@author: Max Weise
"""

from typing import Protocol


class DatabaseItem(Protocol):
    """Convert items to a format that can be saved in a database."""

    def to_tuple(self) -> tuple:
        """Return a tuple that holds all attributes of an object."""
        raise NotImplementedError(
            f"This method is not implemented for type {self}."
        )
