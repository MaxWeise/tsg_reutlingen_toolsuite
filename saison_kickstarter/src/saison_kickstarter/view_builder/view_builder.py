"""Define a common interface to contruct overviews.

Created: 18.02.2024
@author: Max Weise
"""

from typing import Protocol

from saison_kickstarter import tournament

OverviewEntry = tuple[str, str, bool]


class ViewBuilder(Protocol):
    """An interface to provide methods to structure data.

    Data that needs to be written in an excel file should follow a structure,
    that is dependant on the file format and the requirements of the user.
    ViewBuilder classes provide the formatting to write data into their
    destined locations.
    """

    def build_tournament_overview(
        self,
        data: list[tournament.Tournament],
        include_optional_tournaments: bool = True,
    ) -> list[OverviewEntry]:
        """Convert a list of tournaments to be written to an excel file.

        Args:
            data: The list of tournaments to be included in the overview.
            include_optional_tournaments: Set this flag to include or exclude
                optional tournaments in the overview. Defaults to True.

        Returns:
            A list of tuples, structuring the data to be written into rows
            of an excel sheet.
        """
        raise NotImplementedError(
            f"This method is not implemented for type {self}"
        )
