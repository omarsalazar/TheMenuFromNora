from django.db import models


class Clients(models.Model):
    slack_id = models.CharField(max_length=250)
    username = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.username}: {self.slack_id}"
