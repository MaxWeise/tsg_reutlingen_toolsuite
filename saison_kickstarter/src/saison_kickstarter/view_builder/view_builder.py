"""Define a common interface to contruct overviews.

Created: 18.02.2024
@author: Max Weise
"""

from typing import Protocol

from saison_kickstarter import tournament


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
    ) -> list[tuple[str, ...]]:
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
