import factory
from CornershopTest.clients.models import Clients


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clients

    slack_id = factory.Sequence(lambda n: f"slack_id_{n}")
    username = factory.Sequence(lambda n: f"username_{n}")
