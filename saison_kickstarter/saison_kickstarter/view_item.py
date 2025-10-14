"""Defines data classes for different views of tournament information.

This module provides data structures for representing items in various "views"
of the tournament schedule. Each class is designed to hold formatted data
ready for display or output, for example, in a spreadsheet.

The `ViewItem` protocol establishes a common interface, ensuring that all view
item classes can be in turn converted to a tuple for easy serialization into a
tabular format.
"""

import dataclasses
import datetime
import typing
from typing import Iterable, Literal


class ViewItem(typing.Protocol):
    """A protocoll to make a reference point for ViewItem classes."""

    @property
    def is_optional(self) -> bool:
        """Denote if an entry is optional or not."""
        raise NotImplementedError()

    def to_tuple(self) -> tuple[str, ...]:
        """Return the data in the object as an iterable tuple."""
        raise NotImplementedError()


@dataclasses.dataclass(order=True, frozen=True)
class HeaderViewItem:
    _header_cols: Iterable[str]

    @property
    def is_optional(self) -> bool:
        """Denote if an entry is optional or not."""
        return False

    def to_tuple(self) -> tuple[str, ...]:
        return tuple(self._header_cols)

@dataclasses.dataclass(order=True, frozen=True)
class TournamentViewItem:   # pylint: disable=missing-class-docstring
    first_day: datetime.date
    second_day: datetime.date
    title: str
    _is_optional: bool

    @property
    def is_optional(self) -> bool:
        """Denote if an entry is optional or not."""
        return self._is_optional

    def to_tuple(self) -> tuple[str, str]:
        """Create a tuple representation of the object.

        The tuple is in the format the information will be written in a
        tabular form.

        The information is structured as follows:
            Date of the competition, format: dd./dd.mm.yyyy or dd.mm./dd.mm.yyyy
            Title of the competition (example "RL-U13 City")
            If the tournament is optional for the age_group.

        Returns:
            The information of the object in 3-tuple form.
        """
        return (
            self._parse_date(self.first_day, self.second_day),
            self.title,
        )


    def _parse_date(
            self, first_day: datetime.date, second_day: datetime.date
    ) -> str:
        """Parse the combined day format from two seperate date entries.

        Use this function to set the date format for a tournament view item
        in the correct format.

        Args:
            first_day (datetime.date): The first day of the date.
            second_day (datetime.date): The second day of the date.

        Returns:
            A string in the format dd./dd.mm.yyyy or dd.mm./dd.mm.yyyy if the
            datum spans the last and first day of consecutive months.
        """
        day_one = f"{first_day.day:02d}"
        month_one = f"{first_day.month:02d}"

        day_two = f"{second_day.day:02d}"
        month_two = f"{second_day.month:02d}"

        year = first_day.year
        if month_one == month_two:
            # Short date format
            return f"{day_one}./{day_two}.{month_one}.{year}"
        else:
            # Handle long date format
            return f"{day_one}.{month_one}./{day_two}.{month_two}.{year}"


@dataclasses.dataclass(order=True, frozen=True)
class RefereeViewItem:   # pylint: disable=missing-class-docstring
    day: datetime.date
    city: str
    required_licence: Literal["E/D", "D"]

    @property
    def is_optional(self) -> bool:
        """Denote if an entry is optional or not."""
        return False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RefereeViewItem):
            return NotImplemented
        return self.day == other.day and self.city == other.city

    def __hash__(self) -> int:
        return hash((self.day, self.city))

    def to_tuple(self) -> tuple[str, str, str]:
        """Create a tuple representation of the object.

        The tuple is in the format the information will be written in a
        tabular form.

        The information is structured as follows:
            Date of the competition (format: dd.mm.yyyy)
            City of the competition
            Required licence for the tournament ("E/D" or "D")

        Returns:
            The information of the object in 3-tuple form.
        """
        return(
            self.day.strftime("%d.%m.%Y"),
            self.city,
            self.required_licence
        )
