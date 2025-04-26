"""Classes and methods that provide an interface to define excel tables.

Created: 10.02.2024
@author: Max Weise
"""

from typing import Literal

from saison_kickstarter import tournament, view_item


class ExcelViewBuilder:
    """Define the interface for methods to construct a view."""

    def _transform_entries(
        self,
        tournaments: list[tournament.Tournament],
        optional_tournaments: list[tournament.Tournament] | None = None,
        include_optional_tournaments: bool = True,
    ) -> list[view_item.ViewItem]:
        """Combine lists of mandatory and optional tournaments.

        Returns:
            A combined list of mandatory and optional tournaments. The list will
            be sorted by date.
        """
        optional_tournaments_ = (
            optional_tournaments if optional_tournaments else []
        )
        temp1: list[view_item.ViewItem] = [
            view_item.ViewItem(
                comp.first_day, comp.second_day, comp.title, False
            )
            for comp in tournaments
        ]

        temp2: list[view_item.ViewItem] = []

        if include_optional_tournaments:
            temp2 = [
                view_item.ViewItem(
                    comp.first_day, comp.second_day, comp.title, True
                )
                for comp in optional_tournaments_
            ]

        ret: list[view_item.ViewItem] = sorted(temp1 + temp2)
        return ret

    def build_view(
        self,
        data: list[tournament.Tournament],
        include_optional_tournaments: bool = True,
    ) -> list[view_item.ViewItem]:
        """Convert a list of tournaments to be written to an excel file.

        Args:
            data: The list of tournaments to be included in the overview.
            include_optional_tournaments: Set this flag to include or exclude
                optional tournaments in the overview. Defaults to True.

        Returns:
            A structured output format.
        """
        ret: list[view_item.ViewItem] = []
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
            self._transform_entries(
                u11_tournaments,
                include_optional_tournaments=include_optional_tournaments,
            )
            + self._transform_entries(
                u13_tournaments,
                u15_tournaments,
                include_optional_tournaments=include_optional_tournaments,
            )
            + self._transform_entries(
                u15_tournaments,
                u17_tournaments,
                include_optional_tournaments=include_optional_tournaments,
            )
            + self._transform_entries(
                u17_tournaments,
                u20_tournaments,
                include_optional_tournaments=include_optional_tournaments,
            )
            + self._transform_entries(
                u20_tournaments,
                senior_tournaments,
                include_optional_tournaments=include_optional_tournaments,
            )
            + self._transform_entries(
                senior_tournaments,
                include_optional_tournaments=include_optional_tournaments,
            )
            + self._transform_entries(
                veteran_tournaments,
                include_optional_tournaments=include_optional_tournaments,
            )
        )

        return ret

    def build_referee_view(
        self, data: list[tournament.Tournament]
    ) -> list[view_item.RefereeViewItem]:
        """Structure a list of tournaments to be written to an excel file.

        The tournaments get structured so that for each tournament we get
        two entries, separated by date and map a refereeing licence to it.

        Args:
            data: The list of tournaments to be included in the overview.

        Returns:
            A list of structured tournament data.
        """
        filtered_data: list[tournament.Tournament] = list(
            filter(
                lambda t: not (
                    t.city == "Reutlingen"
                    or t.category == tournament.Category.QB
                    or t.category == tournament.Category.DM
                ),
                data,
            )
        )

        overview_items = []
        for t in filtered_data:
            required_license: Literal["D", "E/D"] = (
                "E/D"
                if t.age_group
                in (tournament.AgeGroup.U11, tournament.AgeGroup.U13)
                else "D"
            )
            entry_day_one = view_item.RefereeViewItem(
                t.first_day, t.city, required_license
            )
            entry_day_two = view_item.RefereeViewItem(
                t.second_day, t.city, required_license
            )
            overview_items.append(entry_day_one)
            overview_items.append(entry_day_two)

        return sorted(overview_items)
