from django.db import models
from django.contrib.auth.models import User


class character_Sheet(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    sheet = models.JSONField()

    def __str__(self):
        return self.name
