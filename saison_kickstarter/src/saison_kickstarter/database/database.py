"""Define an interface to handle database operations.

Concrete implementations for database connections should implement this
interface as it provides the standard CRUD operations.

Classes:
    Database: An interface to define database interactions.

Example:

    >>> database: Database = SqlAdapter("./connection.db")
    >>> item: DatabaseItem = Tournament(
            "01.01.2000",
            "Reutlingen",
            "RL",
            "U17"
        ).to_tuple()
    >>> database.create(item)
    >>> querry = database.read()
    >>> print(querry)
    [ ("01.01.2000", "Reutlingen", "RL", "U17") ]


Created: 14.01.2024
@author: Max Weise
"""

from typing import Any, Protocol

from saison_kickstarter.database import database_item


class Database(Protocol):
    """Provide CRUD methods to interact with a database."""

    def create(self, item: database_item.DatabaseItem) -> None:
        """Create a resouce in the underlying table.

        Args:
            item (DatabaseItem): Any object that can be represented as a tuple.
        """
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )

    def read(self) -> list[Any] | None:
        """Read all values from a database table.

        The table is determined by the object the method is used on.

        Returns:
            A list of entries found in the database. If the database is empty,
            return None.
        """
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )
