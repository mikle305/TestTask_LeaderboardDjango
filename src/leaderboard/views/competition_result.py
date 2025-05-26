from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from leaderboard.serializers import CompetitionRequestSerializer, CompetitionResultSerializer
from leaderboard.services import CompetitionService


class CompetitionResultView(APIView):
    def post(self, request: Request):
        serializer = CompetitionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = CompetitionService.get_results(request_data=serializer.validated_data, current_user=request.user)
            return Response(result)

        except PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except CompetitionService.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
