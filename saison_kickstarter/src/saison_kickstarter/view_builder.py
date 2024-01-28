"""Classes and methods that provide an interface to define excel tables.

Created: 25.01.2024
@author: Max Weise
"""

from saison_kickstarter.tournament import AgeGroup, Tournament


class ViewBuilder:
    """Construct an overview of tournaments for all age groups."""

    def __init__(self) -> None:
        self.tournaments_u11: list[Tournament] = []
        self.tournaments_u13: list[Tournament] = []
        self.tournaments_u15: list[Tournament] = []
        self.tournaments_u17: list[Tournament] = []
        self.tournaments_u20: list[Tournament] = []
        self.tournaments_senior: list[Tournament] = []
        self.tournaments_veteran: list[Tournament] = []

    def set_tournaments(self, tournaments: list[Tournament]) -> None:
        """Set the list of tournaments for the age group u11."""
        for t in tournaments:
            print(f"Handling element {t =}")
            if AgeGroup.U11 in t.age_group:
                self.tournaments_u11.append(t)

            if AgeGroup.U13 in t.age_group:
                self.tournaments_u13.append(t)

            if AgeGroup.U15 in t.age_group:
                self.tournaments_u15.append(t)

            if AgeGroup.U17 in t.age_group:
                self.tournaments_u17.append(t)

            if AgeGroup.U20 in t.age_group:
                self.tournaments_u20.append(t)

            if AgeGroup.SENIOR in t.age_group:
                self.tournaments_senior.append(t)

            if AgeGroup.VETERAN in t.age_group:
                self.tournaments_veteran.append(t)

    def _select_tournaments(
        self, age_group: AgeGroup
    ) -> list[Tournament] | None:
        if age_group == AgeGroup.U11:
            return self.tournaments_u11

        if age_group == AgeGroup.U13:
            return self.tournaments_u13

        if age_group == AgeGroup.U15:
            return self.tournaments_u15

        if age_group == AgeGroup.U17:
            return self.tournaments_u17

        if age_group == AgeGroup.U20:
            return self.tournaments_u20

        if age_group == AgeGroup.SENIOR:
            return self.tournaments_senior

        if age_group == AgeGroup.VETERAN:
            return self.tournaments_veteran

        return None

    def build_block(
        self, age_groups: tuple[AgeGroup, AgeGroup]
    ) -> list[tuple[str, str, bool]] | None:
        """Create a table like structure that can be combined to an overview.

        Returns:
            True if no errors occured.
            False otherwise.
        """
        tournaments: list[Tournament] | None = self._select_tournaments(
            age_groups[0]
        )

        if not tournaments:
            raise ValueError(
                f"There are no tournaments for the age group {age_groups[0].value}"
            )

        optional_tournaments: list[
            Tournament
        ] | None = self._select_tournaments(age_groups[1])

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
