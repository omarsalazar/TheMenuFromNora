from django.db import models

from CornershopTest.clients.models import Clients
from CornershopTest.menus.models import Options


class Orders(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.PROTECT)
    option = models.ForeignKey(Options, on_delete=models.PROTECT)
    instructions = models.TextField(blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.client}, {self.option.name}"
