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


class Database(Protocol):
    """Provide CRUD methods to interact with a database."""

    def execute_statement(self, statement: str) -> Any:
        """Excecute a given sql statement and return its sucessvalue"""
        raise NotImplementedError(
            f"This method is not implemented on tpye {self}."
        )
