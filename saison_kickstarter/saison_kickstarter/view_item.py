# TODO: Include docstring for the file

import abc
import datetime
import dataclasses
from typing import Literal

from saison_kickstarter import tournament


@dataclasses.dataclass
class ViewItem(abc.ABC):
    """Base class that provides a common parent for overview items.

    Attributes:
        date (str): The date in string format.
        name (str): The name of the tournament. Is either a city or title of
            the tournament.
    """

    date: str
    name: str

    def __lt__(self, other) -> bool:
        own_date = datetime.datetime.strptime(self.date, "%d.%m.%Y")
        other_date = datetime.datetime.strptime(other.date, "%d.%m.%Y")
        return own_date < other_date

    def __eq__(self, other) -> bool:
        own_date = datetime.datetime.strptime(self.date, "%d.%m.%Y")
        other_date = datetime.datetime.strptime(other.date, "%d.%m.%Y")
        return own_date == other_date


@dataclasses.dataclass
class TournamentViewItem(ViewItem):

    def __init__(self, t: tournament.Tournament, is_optional: bool) -> None:
        """Initialize a view item from a tournament."""
        self.date = self._parse_date(t.first_day, t.second_day)
        self.name = t.title
        self.is_optional = is_optional

    def _parse_date(
        self, first_day: datetime.date, second_day: datetime.date
    ) -> str:
        """Parse the combined day format from two seperate date entries."""
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


class RefereeViewItem(ViewItem):

    def __init__(
        self, day: str, city: str, required_licence: Literal["D", "E/D"]
    ) -> None:
        """Initialize a view item from a tournament."""
        self.date = day
        self.name = city
        self.required_licence = required_licence
