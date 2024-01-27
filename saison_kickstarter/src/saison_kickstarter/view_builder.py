"""Classes and methods that provide an interface to define excel tables.

Created: 25.01.2024
@author: Max Weise
"""

import datetime

from saison_kickstarter.tournament import AgeGroup, Category, Tournament


class ViewBuilder:
    def __init__(self) -> None:
        self.tournaments_u11: list[Tournament] = []
        self.tournaments_u13: list[Tournament] = []
        self.tournaments_u15: list[Tournament] = []
        self.tournaments_u17: list[Tournament] = []
        self.tournaments_u20: list[Tournament] = []
        self.tournaments_senior: list[Tournament] = []
        self.tournaments_veteran: list[Tournament] = []

    def set_tournaments_u11(self, tournaments: list[Tournament]) -> None:
        """Set the list of tournaments for the age group u11."""
        self.tournaments_u11 = tournaments

    def _select_tournaments(
        self, age_group: AgeGroup
    ) -> list[Tournament] | None:
        if age_group == AgeGroup.U11:
            return self.tournaments_u11

        return None

    def build_block(self, age_group: AgeGroup) -> list[tuple[str, str]] | None:
        """Create a table like structure that can be combined to an overview.

        Returns:
            True if no errors occured.
            False otherwise.
        """
        tournaments: list[Tournament] | None = self._select_tournaments(
            age_group
        )

        if not tournaments:
            # raise an error
            return None

        entries: list[tuple[str, str]] = []
        for tournament in tournaments:
            entries.append(
                (tournament.date.strftime("%d.%m.%Y"), tournament.title)
            )

        return entries
