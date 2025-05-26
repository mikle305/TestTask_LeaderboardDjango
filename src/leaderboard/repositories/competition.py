from django.db.models import Window, F
from django.db.models.functions import Rank
from leaderboard.models import CompetitionResult


class CompetitionRepository:
    @classmethod
    def get_ranked_participants(cls, competition, scenario):
        cls._validate_competition(competition)
        cls._validate_scenario(competition, scenario)

        return list(
            CompetitionResult.objects.filter(competition=competition, scenario=scenario, false_start=False)
            .order_by("flight_time")
            .annotate(position=Window(expression=Rank(), order_by=F("flight_time").asc()))
        )

    @staticmethod
    def _validate_competition(competition):
        if not CompetitionResult.objects.filter(competition=competition).exists():
            raise CompetitionResult.DoesNotExist("Competition not found")

    @staticmethod
    def _validate_scenario(competition, scenario):
        if not CompetitionResult.objects.filter(competition=competition, scenario=scenario).exists():
            raise CompetitionResult.DoesNotExist("Scenario not found")
