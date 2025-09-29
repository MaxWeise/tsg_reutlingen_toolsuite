# TODO: Include docstring for the file

import dataclasses
import datetime
import typing
from typing import Any, Literal


class ViewItem(typing.Protocol):
    """A protocoll to make a reference point for ViewItem classes."""

    def to_tuple(self) -> tuple[str, str, Any]:
        raise NotImplementedError()


@dataclasses.dataclass(order=True, frozen=True)
class TournamentViewItem:
    first_day: datetime.date
    second_day: datetime.date
    title: str
    is_optional: bool

    def to_tuple(self) -> tuple[str, str, bool]:
        """Create a tuple representation of the object.

        The tuple is in the format the information will be written in a
        tabular form.

        The information is structured as follows:
            Date of the competition (format: dd./dd.mm.yyyy or dd.mm./dd.mm.yyyy)
            Title of the competition (example "RL-U13 City")
            If the tournament is optional for the age_group.

        Returns:
            The information of the object in 3-tuple form.
        """
        return (
            self._parse_date(self.first_day, self.second_day),
            self.title,
            self.is_optional
        )


    def _parse_date(self, first_day: datetime.date, second_day: datetime.date) -> str:
        """Parse the combined day format from two seperate date entries.

        Use this function to set the date format for a tournament view item
        in the correct format.

        Args:
            first_day (datetime.date): The first day of the date.
            second_day (datetime.date): The second day of the date.

        Returns:
            A string in the format dd./dd.mm.yyyy or dd.mm./dd.mm.yyyy if the datum
            spans the last and first day of consecutive months.
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
class RefereeViewItem:
    day: datetime.date
    city: str
    required_licence: Literal["E/D", "D"]

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
