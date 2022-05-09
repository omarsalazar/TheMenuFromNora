from rest_framework import serializers

from CornershopTest.clients.models import Clients


class ClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ("id", "username", "slack_id")
        read_only_fields = ("id",)
