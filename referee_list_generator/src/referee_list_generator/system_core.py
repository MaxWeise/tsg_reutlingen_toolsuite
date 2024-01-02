"""Classes and fuctions which are the low level building blocks of the scirpt.

Created: 23.12.2023
@author: Max Weise
"""

import dataclasses


@dataclasses.dataclass
class ExcelWriteError(Exception):
    """When an exception is raised while trying to write to an excel file.

    Args:
        message (str): The message raised by the previous exception.
    """

    message: str


@dataclasses.dataclass
class MissingArgumentError(Exception):
    """When a cli argument was not passed to the programm.

    Args:
        message (str): The message raised by the previous exception.
    """

    message: str


@dataclasses.dataclass
class DataRow:
    """A row in a spreadsheet holding information about a referee.

    Attributes:
        last_name: The last name of the person. Used as primary key.
        first_name: The filst name of the person.
        year_of_birth: The year in which the person was born.
        training_D_licence: Wheather or not the person has completet
            the training for the regional D-licence.
        obtained_D_licence: Wheather or not the person has obtained the
            regional refereeing-licence.
        training_CN_licence: Wheather or not the person has completet
            the training for the national CN-licence.
        obtained_CN_licence: Wheather or not the person has obtained the
            national refereeing-licence.
    """

    last_name: str
    first_name: str
    year_of_birth: str
    _training_d_licence: bool = False
    _obtained_d_licence: bool = False
    _expiration_date_d_licence: str | None = None
    _training_cn_licence: bool = False
    _obtained_cn_licence: bool = False

    @property
    def begun_training_d_licence(self) -> str:
        """Map the property to a human readable string."""
        return "Ja" if self._training_d_licence else "Nein"

    @property
    def obtained_d_licence(self) -> str:
        """Map the property to a human readable string."""
        return "Ja" if self._obtained_d_licence else "Nein"

    @property
    def expiration_date_d_licence(self) -> str:
        """Map the property to a human readable string."""
        return (
            "---"
            if self._expiration_date_d_licence is None
            else str(self._expiration_date_d_licence)
        )

    @property
    def training_cn_licence(self) -> str:
        """Map the property to a human readable string."""
        return "Ja" if self._training_cn_licence else "Nein"

    @property
    def obtained_cn_licence(self) -> str:
        """Map the property to a human readable string."""
        return "Ja" if self._obtained_cn_licence else "Nein"


class Maybe:
    """Monad-like class that handles errors through none values.

    Attributes:
        _value (T): The value of the monad type.
    """

    def __init__(self, value):
        """Initialize a Maybe instance.

        Args:
            value (T): The value of the maybe-instance.
        """
        self._value = value

    @property
    def value(self):
        """The value of the monad."""
        return self._value

    def bind(self, func):
        """Apply a function to the internal value.

        In case of errors or missing values, a function should return no value.
        The Maybe monad propagates the error / missing value thorughout the
        programm.

        Args:
            func (T -> U | None): A function that takes a value and returns
                a new value or none.

        Returns:
            result (Maybe<T | None>): A monad object that holds the result of
                the computation done by func.
        """
        if self._value is None:
            return Maybe(None)

        result = func(self._value)
        return Maybe(result)
