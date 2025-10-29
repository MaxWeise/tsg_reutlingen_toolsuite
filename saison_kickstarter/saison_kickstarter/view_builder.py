"""Define classes to construct a view-dataformat.

Created: 18.02.2024
@author: Max Weise
"""

import functools
import itertools
from typing import Literal, Protocol, Sequence

from saison_kickstarter import tournament, view_item


class ViewBuilder(Protocol):
    """An interface to provide methods to structure data.

    Data needs to be structured according to the output format. Componentes
    of type ViewBuilder are tasked with organizing in such a way, that the
    output format can display them in a correct way.
    """

    def build_view(
        self,
        data: list[tournament.Tournament],
    ) -> Sequence[view_item.ViewItem]:
        """Convert a list of tournaments to be written to an excel file.

        Args:
            data: The list of tournaments to be included in the overview.
            include_optional_tournaments: Set this flag to include or exclude
                optional tournaments in the overview. Defaults to True.

        Returns:
            A structured output format.
        """
        raise NotImplementedError(
            f"This method is not implemented for type {self}"
        )


class TournamentViewBuilder:
    """Define the interface for methods to construct a view."""

    def __init__(self, include_optional: bool) -> None:
        """Initialize the object.

        Args:
            include_optional (bool): If optional tournaments should be
                included in the view.
        """
        self._include_optonal = include_optional
        self._inclusion_criteria_nonoptional: dict[
            tournament.AgeGroup, tuple[tournament.AgeGroup, ...]
        ] = {
            tournament.AgeGroup.U11: (tournament.AgeGroup.U11,),
            tournament.AgeGroup.U13: (tournament.AgeGroup.U13,),
            tournament.AgeGroup.U15: (tournament.AgeGroup.U15,),
            tournament.AgeGroup.U17: (tournament.AgeGroup.U17,),
            tournament.AgeGroup.U20: (tournament.AgeGroup.U20,),
            tournament.AgeGroup.SENIOR: (tournament.AgeGroup.SENIOR,),
            tournament.AgeGroup.VETERAN: (tournament.AgeGroup.VETERAN,),
        }
        self._inclusion_criteria_optional: dict[
            tournament.AgeGroup, tuple[tournament.AgeGroup, ...]
        ] = {
            tournament.AgeGroup.U11: (tournament.AgeGroup.U11,),
            tournament.AgeGroup.U13: (
                tournament.AgeGroup.U13,
                tournament.AgeGroup.U15,
            ),
            tournament.AgeGroup.U15: (
                tournament.AgeGroup.U15,
                tournament.AgeGroup.U17,
            ),
            tournament.AgeGroup.U17: (
                tournament.AgeGroup.U17,
                tournament.AgeGroup.U20,
            ),
            tournament.AgeGroup.U20: (
                tournament.AgeGroup.U20,
                tournament.AgeGroup.SENIOR,
            ),
            tournament.AgeGroup.SENIOR: (tournament.AgeGroup.SENIOR,),
            tournament.AgeGroup.VETERAN: (tournament.AgeGroup.VETERAN,),
        }

    def _filter_for_age_group(self,
                              t: tournament.Tournament,
                              lut: dict,
                              ag: tournament.AgeGroup) -> bool:
        """Define the filter criterium for ViewItems.

        This function is intended to be used in a filter.

        Args:
            t: A tournament object.
            lut: A lookup-table that maps an AgeGroup to a tuple of AgeGroups
                that may start at a competition under the given AgeGroup.
            ag: The specific AgeGrop to filter for.

        Returns:
            Whether or not a tournament is in the range of given AgeGroups.
        """
        return t.age_group in lut[ag]

    def build_view(
        self,
        data: list[tournament.Tournament],
    ) -> Sequence[view_item.ViewItem]:
        """Create a list of TournamentViewItems from a list of tournaments.

        The ViewItems can be used by a writer class and be written to an excel
        file. The method also sets the is_optional flag for each tournament
        according to the age group.

        Args:
            data: The list of tournaments to be included in the overview.
            include_optional_tournaments: Set this flag to include or exclude
                optional tournaments in the overview. Defaults to True.

        Returns:
            A structured output format.
        """
        ret = []
        age_group_lut: dict[
            tournament.AgeGroup, tuple[tournament.AgeGroup, ...]
        ] = (
            self._inclusion_criteria_optional
            if self._include_optonal
            else self._inclusion_criteria_nonoptional
        )

        filter_func = functools.partial(
            self._filter_for_age_group,
            lut=age_group_lut
        )

        for ag in tournament.AgeGroup:
            filter_func = functools.partial(filter_func, ag=ag)
            vi: list[view_item.TournamentViewItem] = [  # type: ignore
                view_item.TournamentViewItem(
                    t.first_day,
                    t.second_day,
                    t.title,
                    False if ag == t.age_group else True,
                ) for t in filter(filter_func, data)
            ]
            ret.append(sorted(vi))

        return list(itertools.chain(*ret))


class RefereeViewBuilder:
    """Create an overview for referees to plan their appointments."""

    def _filter_condition(self, t: tournament.Tournament) -> bool:
        """Filter out tournaments that meet specific criteria:

        Tournaments are not included if they:
            - Take place in Reutlingen, as referees get appointed seperately
            - Have a category of QB or DM, as those require another type of
                licence. Referees also get appointed seperately.

        Args:
            t: A tournament that gets checked for the criteria.

        Returns:
            True, if a tournament is to be included in the overview.
            False otherwise.
        """
        return not (
            t.city == "Reutlingen"
            or t.category == tournament.Category.QB
            or t.category == tournament.Category.DM
        )

    def build_view(
        self, data: list[tournament.Tournament]
    ) -> Sequence[view_item.ViewItem]:
        """Structure a list of tournaments to be written to an excel file.

        The tournaments get structured so that for each tournament we get
        two entries, separated by date and map a refereeing licence to it.

        Args:
            data: The list of tournaments to be included in the overview.

        Returns:
            A list of structured tournament data.
        """

        ret: list[view_item.RefereeViewItem] = []
        for t in filter(self._filter_condition, data):
            required_licence: Literal["D", "E/D"] = (
                "E/D"
                if t.age_group
                in (tournament.AgeGroup.U11, tournament.AgeGroup.U13)
                else "D"
            )
            entry_one = view_item.RefereeViewItem(
                t.first_day, t.city, required_licence
            )
            entry_two = view_item.RefereeViewItem(
                t.second_day, t.city, required_licence
            )
            ret.append(entry_one)
            ret.append(entry_two)

        return sorted(set(ret))
