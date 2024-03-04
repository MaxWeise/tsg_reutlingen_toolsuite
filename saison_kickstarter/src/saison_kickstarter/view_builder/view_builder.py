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
        raise NotImplementedError(
            f"This method is not implemented for type {self}"
        )
