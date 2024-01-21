"""Definition of a tournament data entry.

Created: 14.01.2024
@author: Max Weise
"""

import dataclasses
import datetime
import enum
import itertools


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
    date: datetime.datetime
    city: str
    category: Category
    age_group: set[AgeGroup]
    _identifier: int = dataclasses.field(
        default_factory=itertools.count().__next__
    )

    def to_tuple(self) -> tuple:
        age_groups = " ".join([ag.value for ag in self.age_group])
        return (
            self._identifier,
            self.date,
            self.city,
            self.category.value,
            age_groups,
        )
