"""Definition of a tournament data entry.

Created: 14.01.2024
@author: Max Weise
"""

import dataclasses
import datetime
import enum


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
    SENIOR = "Senior"
    VETERAN = "Veteran"


@dataclasses.dataclass
class Tournament:
    """Representation of a tournament in the database."""

    date: datetime.date
    city: str
    category: Category
    age_group: AgeGroup

    def to_tuple(self) -> tuple[datetime.date, str, str, str]:
        """Convert a tournament to a tuple.

        Returns:
            The data of the tournament object in form of a tuple.
        """
        return (
            self.date,
            self.city,
            self.category.value,
            self.age_group.value,
        )

    @property
    def title(self) -> str:
        """The full title of the tournament"""
        seperator = "-" if self.category == Category.RL else " "
        category = self.category.value
        age_group = self.age_group.value
        ret = f"{category}{seperator}{age_group} {self.city}"
        return ret


def _category_from_string(category: str) -> Category:
    categories = {
        "BNWM": Category.BNWM,
        "DM": Category.DM,
        "RL": Category.RL,
        "QB": Category.QB,
    }

    return categories[category]


def _age_group_from_string(age_group: str) -> AgeGroup:
    age_groups = {
        "u11": AgeGroup.U11,
        "u13": AgeGroup.U13,
        "u15": AgeGroup.U15,
        "u17": AgeGroup.U17,
        "u20": AgeGroup.U20,
        "senior": AgeGroup.SENIOR,
        "senioren": AgeGroup.SENIOR,
        "veteran": AgeGroup.VETERAN,
        "veteranen": AgeGroup.VETERAN,
    }

    return age_groups[age_group.lower()]


def _date_from_string(date: str, sql_date_format: bool) -> datetime.date:
    """Construct a datetime object from a string.

    SQL saves the date as yyyy-mm-dd. To handle this special case, a flag
    is used to determine which date-format is used and how the date should be
    retrieved from the string.

    Args:
        date (str): The date as string.
        sql_date_format (bool): Wether the date is in yyyy-mm-dd format.

    Returns:
        A datetime object that holds the data from the string.
    """
    date_seperator = "-" if sql_date_format else "."
    parts = date.split(date_seperator)

    if sql_date_format:
        parts.reverse()

    day, month, year = parts
    return datetime.date(year=int(year), month=int(month), day=int(day))


def tournament_from_tuple(
    entries: tuple[str, str, str, str], sql_date_format: bool = False
) -> Tournament:
    """Construct a tournament object from a tuple of entries.

    Args:
        entries: A tuple of data that will be converted
            into a tournament object.
        sql_data_format (bool, optional): If the dateformat is yyyy-mm-dd.
            Defaults to False

    Returns:
        A tournament containing the data from entries.
    """
    date = _date_from_string(entries[0], sql_date_format)
    city = entries[1]
    category = _category_from_string(entries[2])
    age_groups = _age_group_from_string(entries[3])

    return Tournament(
        date=date,
        city=city,
        category=category,
        age_group=age_groups,
    )
