from rest_framework import serializers


class CompetitionResultSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    user_name = serializers.CharField()
    flight_time = serializers.FloatField()
    command_name = serializers.CharField()
