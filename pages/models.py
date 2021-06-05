from django.db import models
from django.contrib.auth import get_user_model


class character_Sheet(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    name = models.CharField("name", max_length=255, default=None)
    clas = models.CharField("class", max_length=255, default=None)
    race = models.CharField("race", max_length=255, default=None)
    level = models.IntegerField("level", default=None)
    sheet = models.JSONField("character sheet")


