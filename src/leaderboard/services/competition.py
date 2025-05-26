from django.db import transaction
from leaderboard.repositories import CompetitionRepository
from leaderboard.models import CompetitionResult
from common.env_settings import env_settings


class CompetitionService:
    class NotFoundError(Exception):
        pass

    @classmethod
    @transaction.atomic
    def get_results(cls, request_data: dict, current_user):
        cls._validate_permissions(request_data, current_user)

        try:
            participants = CompetitionRepository.get_ranked_participants(
                request_data["competition"], request_data["scenario"]
            )
        except CompetitionResult.DoesNotExist as e:
            raise cls.NotFoundError(str(e))

        user_result = next((p for p in participants if p.user_name == request_data["user_name"]), None)
        if not user_result:
            raise cls.NotFoundError("User result not found")

        return cls._format_response(user_result, participants)

    @classmethod
    def _validate_permissions(cls, data, user):
        if not user.is_superuser and data["user_name"] != user.username:
            raise PermissionError("Not enough rights to check another user's results")

    @classmethod
    def _format_response(cls, user_result, participants):
        other_results = [p for p in participants if p.user_name != user_result.user_name][
            : env_settings.app.results_count - 1
        ]

        return {
            "user_result": cls._serialize_result(user_result),
            "other_results": [cls._serialize_result(p) for p in other_results],
        }

    @staticmethod
    def _serialize_result(result):
        return {
            "position": result.position,
            "user_name": result.user_name,
            "flight_time": result.flight_time,
            "command_name": result.command_name,
        }
