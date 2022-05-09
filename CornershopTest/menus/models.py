import uuid

from django.db import models


class Options(models.Model):
    name = models.CharField(max_length=250, blank=False)
    content = models.TextField()

    class Meta:
        verbose_name = "option"
        verbose_name_plural = "options"

    def __str__(self):
        return self.name


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    options = models.ManyToManyField(Options)
    date = models.DateField(unique=True)

    def __str__(self):
        return f"{self.date} menu"
