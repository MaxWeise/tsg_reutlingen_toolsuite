"""Definition of a tournament data entry.

Created: 14.01.2024
@author: Max Weise
"""

import dataclasses
import datetime
import enum

import pydantic


class Category(enum.Enum):
    """Different kinds of tournaments.

    Each tournament belongs to a category. This dictates how fencers need to
    qualify and what referee licence is needed.
    """

    BNWM = "BNWM"
    DM = "DM"
    RL = "RL"
    # This is not the correct nomenclature
    # We keep it, as it is only important when writing to excel
    QB = "QB"


class AgeGroup(enum.Enum):
    """Possible age groups for a tournament."""

    U11 = "U11"
    U13 = "U13"
    U15 = "U15"
    U17 = "U17"
    U20 = "U20"
    SENIOR = "Senioren"
    VETERAN = "Veteranen"


class Tournament(pydantic.BaseModel):
    """Representation of a tournament in the database."""

    first_day: datetime.date
    second_day: datetime.date
    city: str
    category: Category
    age_group: AgeGroup

    def _get_title_qb(self) -> str:
        """Construct the title for national qualification tournaments.

        Returns:
            The title formatted according to the nomenclature.
        """
        if self.age_group == AgeGroup.SENIOR:
            return f"{self.category.value} {self.city}"

        return f"{self.age_group.value}Q {self.city}"

    @property
    def title(self) -> str:
        """The full title of the tournament"""
        seperator = "-" if self.category == Category.RL else " "

        if self.category == Category.QB:
            return self._get_title_qb()

        age_group = self.age_group.value[0:3]  # shortened version for senior
        return f"{self.category.value}{seperator}{age_group} {self.city}"

    def __hash__(self) -> int:
        return hash(
            (
                self.first_day,
                self.second_day,
                self.city,
                self.category.value,
                self.age_group,
            )
        )


def date_from_string(date: str) -> datetime.date:
    """Construct a datetime object from a string.

    SQL saves the date as yyyy-mm-dd. To handle this special case, a flag
    is used to determine which date-format is used and how the date should be
    retrieved from the string.

    Args:
        date (str): The date as string.

    Returns:
        A datetime object that holds the data from the string.
    """
    date_seperator = "."
    parts = date.split(date_seperator)

    day, month, year = parts
    return datetime.date(year=int(year), month=int(month), day=int(day))


def _get_two_dates_from_string(date: str) -> tuple[str, str]:
    """Parse the date from a combined view to two seperate dates.

    Normally the input will be in a dd./dd.mm.yyyy or in a dd.mm/dd.mm.yyyy
    format. This needs to be parsed to two seperate entrys for the
    tournament object.

    Args:
        date (str): The date in the combined dd./dd.mm.yyyy or
            dd.mm/dd.mm.yyyy format.

    Returns:
        A tuple containing the two date entrys in dd.mm.yyyy format.

    Raises:
        ValueError: The date is in the wrong format.
    """

    if len(date) < 14:
        raise ValueError(
            f"Wrong date-format recieved: {date}."
            "\nDate should follow either"
            " dd./dd.mm.yyyy or dd.mm./dd.mm.yyyy format!"
        )

    parts_uncleaned = date.split(".")
    parts = [part.replace("/", "") for part in parts_uncleaned]

    if len(date) == 14:
        # Handle Weekend in same month
        first_day, second_day, month, year = parts

        return (
            f"{first_day}.{month}.{year}",
            f"{second_day}.{month}.{year}",
        )
    else:
        first_day, first_month, second_day, second_month, year = parts
        return (
            f"{first_day}.{first_month}.{year}",
            f"{second_day}.{second_month}.{year}",
        )


def tournament_from_tuple(data: tuple[str, str, str, str]) -> Tournament:
    """Construct a tournament from a tuple object.

    This function is used as a helper function and converts the arguments
    from the tuple to the needed types.

    Args:
        data (tuple[str, str, str, str]): A tuple containing the data for
            the tournaments.

    Returns:
        A tournament object holding the data of the tuple.
    """
    date, city, category, age_group = data
    dates = _get_two_dates_from_string(date)
    fd = date_from_string(dates[0])
    sd = date_from_string(dates[1])

    cat = Category(category)
    age = AgeGroup(age_group)

    return Tournament(
        first_day=fd,
        second_day=sd,
        city=city,
        category=cat,
        age_group=age,
    )
