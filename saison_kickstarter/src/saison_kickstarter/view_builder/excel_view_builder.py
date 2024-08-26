"""Classes and methods that provide an interface to define excel tables.

Created: 10.02.2024
@author: Max Weise
"""

import dataclasses
import datetime

from saison_kickstarter import tournament

OverviewEntry = tuple[str, str, bool]


@dataclasses.dataclass(order=True)
class _OverviewEntryItem:
    """Helper class to define order an order for the entry items.

    Attributes:
        date (datetime.date): Date of the competition.
        competition_name (str): Name of the competition, must adhere to
            nomenclature.
        is_optional (bool): Whether or not the tournament is optional
            for the current age group.
    """

    date: datetime.date
    competition_name: str
    is_optional: bool

    def __lq__(self, other) -> bool:
        return self.date < other.date

    def to_tuple(self) -> OverviewEntry:
        """Convert the object to a tuple.

        Returns:
            The object represented as a tuple.
        """
        return (
            self.date.strftime("%d.%m.%Y"),
            self.competition_name,
            self.is_optional,
        )


class ExcelViewBuilder:
    """Define the interface for methods to construct a view."""

    def _transform_entries(
        self,
        tournaments: list[tournament.Tournament],
        optional_tournaments: list[tournament.Tournament] | None = None,
    ) -> list[OverviewEntry]:
        """Combine lists of mandatory and optional tournaments.

        Returns:
            A combined list of mandatory and optional tournaments. The list will
            be sorted by date.
        """
        optional_tournaments_ = (
            optional_tournaments if optional_tournaments else []
        )
        temp1: list[_OverviewEntryItem] = [
            _OverviewEntryItem(comp.date, comp.title, False)
            for comp in tournaments
        ]
        temp2: list[_OverviewEntryItem] = [
            _OverviewEntryItem(comp.date, comp.title, True)
            for comp in optional_tournaments_
        ]

        ret: list[OverviewEntry] = [
            comp.to_tuple() for comp in sorted(temp1 + temp2)
        ]
        return ret

    def build_tournament_overview(
        self, data: list[tournament.Tournament]
    ) -> list[OverviewEntry]:
        """[See base class]."""
        ret: list[OverviewEntry] = []
        u11_tournaments: list[tournament.Tournament] = list(
            filter(lambda t: t.age_group == tournament.AgeGroup.U11, data)
        )
        u13_tournaments: list[tournament.Tournament] = list(
            filter(lambda t: t.age_group == tournament.AgeGroup.U13, data)
        )
        u15_tournaments: list[tournament.Tournament] = list(
            filter(lambda t: t.age_group == tournament.AgeGroup.U15, data)
        )
        u17_tournaments: list[tournament.Tournament] = list(
            filter(lambda t: t.age_group == tournament.AgeGroup.U17, data)
        )
        u20_tournaments: list[tournament.Tournament] = list(
            filter(lambda t: t.age_group == tournament.AgeGroup.U20, data)
        )
        senior_tournaments: list[tournament.Tournament] = list(
            filter(lambda t: t.age_group == tournament.AgeGroup.SENIOR, data)
        )
        veteran_tournaments: list[tournament.Tournament] = list(
            filter(lambda t: t.age_group == tournament.AgeGroup.VETERAN, data)
        )

        ret = (
            self._transform_entries(u11_tournaments)
            + self._transform_entries(u13_tournaments, u15_tournaments)
            + self._transform_entries(u15_tournaments, u17_tournaments)
            + self._transform_entries(u17_tournaments, u20_tournaments)
            + self._transform_entries(u20_tournaments, senior_tournaments)
            + self._transform_entries(senior_tournaments)
            + self._transform_entries(veteran_tournaments)
        )

        return ret
