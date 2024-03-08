"""Define a common interface to contruct overviews.

Created: 18.02.2024
@author: Max Weise
"""

from typing import Protocol

from saison_kickstarter.tournament import Tournament

OverviewEntry = tuple[str, str, bool]


class ViewBuilder(Protocol):

    def build_tournament_overview(
        self, data: list[Tournament]
    ) -> list[OverviewEntry]:
        """Convert a list of tournaments to be written to an excel file.

        Args:
            data: The list of tournaments to be included in the overview.

        Returns:
            A list of tuples, structuring the data to be written into rows
            of an excel sheet.
        """
        raise NotImplementedError(
            f"This method is not implemented for type {self}"
        )
