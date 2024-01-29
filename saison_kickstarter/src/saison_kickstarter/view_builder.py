"""Classes and methods that provide an interface to define excel tables.

Created: 25.01.2024
@author: Max Weise
"""

from saison_kickstarter.tournament import AgeGroup, Tournament


class ViewBuilder:
    """Construct an overview of tournaments for all age groups."""

    def __init__(self) -> None:
        self.tournaments: dict[AgeGroup, list[Tournament]] = {
            AgeGroup.U11: [],
            AgeGroup.U13: [],
            AgeGroup.U15: [],
            AgeGroup.U17: [],
            AgeGroup.U20: [],
            AgeGroup.SENIOR: [],
            AgeGroup.VETERAN: [],
        }

    def set_tournaments(self, tournaments: list[Tournament]) -> None:
        """Set the list of tournaments for the age group u11."""
        for t in tournaments:
            for ag in t.age_group:
                self.tournaments[ag].append(t)

    def build_block(
        self, age_groups: tuple[AgeGroup, AgeGroup]
    ) -> list[tuple[str, str, bool]] | None:
        """Create a table like structure that can be combined to an overview.

        Returns:
            True if no errors occured.
            False otherwise.
        """
        tournaments: list[Tournament] = self.tournaments[age_groups[0]]

        if not tournaments:
            raise ValueError(
                f"There are no tournaments for the age group {age_groups[0].value}"
            )

        optional_tournaments: list[Tournament] = self.tournaments[age_groups[1]]

        entries: list[tuple[str, str, bool]] = []
        for tournament in tournaments:
            entries.append(
                (tournament.date.strftime("%d.%m.%Y"), tournament.title, False)
            )

        if optional_tournaments:
            for tournament in optional_tournaments:
                entries.append(
                    (
                        tournament.date.strftime("%d.%m.%Y"),
                        tournament.title,
                        True,
                    )
                )

        return sorted(entries)
