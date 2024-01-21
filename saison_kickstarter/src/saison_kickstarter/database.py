"""Define an interface to handle database operations.

Concrete implementations for database connections should implement this
interface as it provides the standard CRUD operations.

Standart usecase:

    database: Database = SqlAdapter("./connection.db")
    database.create("table", item")


Created: 14.01.2024
@author: Max Weise
"""

from typing import Any, Protocol

from saison_kickstarter.database_item import DatabaseItem


class Database(Protocol):
    """Provide CRUD methods to interact with a database."""

    def create(self, item: DatabaseItem) -> bool | None:
        """Create a resouce in the underlying table."""
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )

    def read(self) -> list[Any] | None:
        """Read all values from a database table."""
        raise NotImplementedError(
            f"The method is not implemented for type {self}"
        )
