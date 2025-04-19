"""Define a common structure for different overview formats.

The data provided by the overview does not change with the format. Everytime,
the overview communicates the date(s) of a tournamant, the name of the
tournament, which includes the category, age group and city, and if the
tournament is optional for the current age group.

These informations will be structured in one class in this file.

Created: 18.04.2025
@author: Max Weise
"""

import dataclasses
import datetime


@dataclasses.dataclass(order=True)
class ViewItem:
    """Helper class to define order an order for the entry items.

    Attributes:
        date (str): Date of the competition.
        competition_name (str): Name of the competition, must adhere to
            nomenclature.
        is_optional (bool): Whether or not the tournament is optional
            for the current age group.
    """

    def __init__(
        self,
        first_day: datetime.date,
        second_day: datetime.date,
        competitin_name: str,
        is_optional: bool,
    ) -> None:
        """Initialize the class.

        The date gets combined in a representation that shows two dates at once.

        Args:
            first_day (datetime.date): The first day of the competition.
            second_day (datetime.date): The second day of the competition.
            city (str): The city the competition takes place in.
            category (Category): Whether the competition is a Championshitp or
                Qualifier tournament.
            age_group (AgeGroup): The primary age group for the competition.
        """
        self._first_day = first_day
        self.competition_name = competitin_name
        self.is_optional = is_optional

        day_one = f"{first_day.day:02d}"
        month_one = f"{first_day.month:02d}"

        day_two = f"{second_day.day:02d}"
        month_two = f"{second_day.month:02d}"

        year = first_day.year
        if month_one == month_two:
            # Short date format
            self.date = f"{day_one}./{day_two}.{month_one}.{year}"
        else:
            # Handle long date format
            self.date = f"{day_one}.{month_one}./{day_two}.{month_two}.{year}"

    def __lq__(self, other) -> bool:
        return self._first_day < other._first_day
