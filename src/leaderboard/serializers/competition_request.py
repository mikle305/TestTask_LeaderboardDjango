from rest_framework import serializers


class CompetitionRequestSerializer(serializers.Serializer):
    competition = serializers.CharField()
    user_name = serializers.CharField()
    scenario = serializers.CharField()
