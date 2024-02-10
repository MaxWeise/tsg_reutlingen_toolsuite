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

    identifier: int
    date: datetime.date
    city: str
    category: Category
    age_group: AgeGroup

    def to_tuple(self) -> tuple[int, datetime.date, str, str, str]:
        return (
            self.identifier,
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
        "U11": AgeGroup.U11,
        "U13": AgeGroup.U13,
        "U15": AgeGroup.U15,
        "U17": AgeGroup.U17,
        "U20": AgeGroup.U20,
        "Senior": AgeGroup.SENIOR,
        "Veteran": AgeGroup.VETERAN,
    }

    return age_groups[age_group]


def tournament_from_tuple(
    entries: tuple[int, str, str, str, str]
) -> Tournament:
    """Construct a tournament object from a tuple of entries."""
    identifier = entries[0]
    date = datetime.datetime.strptime(entries[1], "%y-%m-%d %H:%M:%S")
    city = entries[2]
    category = _category_from_string(entries[3])
    age_groups = _age_group_from_string(entries[4])

    return Tournament(
        identifier=identifier,
        date=date,
        city=city,
        category=category,
        age_group=age_groups,
    )
