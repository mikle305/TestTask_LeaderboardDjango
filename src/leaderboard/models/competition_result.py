from django.db import models


class CompetitionResult(models.Model):
    competition = models.CharField(max_length=255, db_index=True)
    room_id = models.CharField(max_length=255)
    command_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    scenario = models.CharField(max_length=255, db_index=True)
    flight_time = models.FloatField(db_index=True)
    false_start = models.BooleanField(default=False)
