"""Classes and methods that provide an interface to define excel tables.

Created: 10.02.2024
@author: Max Weise
"""

from saison_kickstarter import tournament

OverviewEntry = tuple[str, str, bool]


class ExcelViewBuilder:
    """Define the interface for methods to construct a view."""

    def _transform_entries(
        self,
        tournaments: list[tournament.Tournament],
        optional_tournaments: list[tournament.Tournament] | None = None,
    ) -> list[OverviewEntry]:
        ret = []

        for tournament in tournaments:
            ret.append(
                (tournament.date.strftime("%d.%m.%Y"), tournament.title, False)
            )

        # Early return
        if not optional_tournaments:
            return ret

        for tournament in optional_tournaments:
            ret.append(
                (
                    tournament.date.strftime("%d.%m.%Y"),
                    tournament.title,
                    True,
                )
            )

        return ret

    def build_tournament_overview(
        self, data: list[tournament.Tournament]
    ) -> list[OverviewEntry]:
        """[See base class]."""
        ret: list[OverviewEntry] = []

        u11_tournaments = list(
            filter(lambda t: t.age_group == tournament.AgeGroup.U11, data)
        )
        u13_tournaments = list(
            filter(lambda t: t.age_group == tournament.AgeGroup.U13, data)
        )
        u15_tournaments = list(
            filter(lambda t: t.age_group == tournament.AgeGroup.U15, data)
        )
        u17_tournaments = list(
            filter(lambda t: t.age_group == tournament.AgeGroup.U17, data)
        )
        u20_tournaments = list(
            filter(lambda t: t.age_group == tournament.AgeGroup.U20, data)
        )
        senior_tournaments = list(
            filter(lambda t: t.age_group == tournament.AgeGroup.SENIOR, data)
        )
        veteran_tournaments = list(
            filter(lambda t: t.age_group == tournament.AgeGroup.VETERAN, data)
        )

        ret = (
            self._transform_entries(u11_tournaments)
            + self._transform_entries(u13_tournaments, u15_tournaments)
            + self._transform_entries(u15_tournaments, u17_tournaments)
            + self._transform_entries(u17_tournaments, u20_tournaments)
            + self._transform_entries(u20_tournaments, senior_tournaments)
            + self._transform_entries(senior_tournaments)
            + self._transform_entries(veteran_tournaments)
        )

        return ret
