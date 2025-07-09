"""Define classes to construct a view-dataformat.

Created: 18.02.2024
@author: Max Weise
"""

from typing import Literal, Protocol

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

    def build_view(
        self,
        data: list[tournament.Tournament],
        include_optional_tournaments: bool = True,
    ) -> list[view_item.TournamentViewItem]:
        """Convert a list of tournaments to be written to an excel file.

        Args:
            data: The list of tournaments to be included in the overview.
            include_optional_tournaments: Set this flag to include or exclude
                optional tournaments in the overview. Defaults to True.

        Returns:
            A structured output format.
        """
        # TODO: Implement method. Work incrementally by implementing for one age group + optional
        #       and then implementing for all agegroups + optional

        # Filter tournaments nach Altersklasse

        # Füge optionale hinzu, falls nötig

        # Erstelle viewItems aus der erhaltenen Turnierliste
        ... 


class RefereeViewBuilder:

    def build_view(
        self, data: list[tournament.Tournament]
    ) -> list[view_item.ViewItem]:
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
                t.first_day.strftime("%d.%m.%Y"), t.city, required_license
            )
            entry_day_two = view_item.RefereeViewItem(
                t.second_day.strftime("%d.%m.%Y"), t.city, required_license
            )

            overview_items.append(entry_day_one)
            overview_items.append(entry_day_two)

        return sorted(overview_items)
