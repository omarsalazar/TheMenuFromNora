from rest_framework import serializers

from CornershopTest.clients.serializers import ClientModelSerializer
from CornershopTest.menus.serializers import OptionsModelSerializer
from CornershopTest.orders.models import Orders


class OrderModelSerializer(serializers.ModelSerializer):
    client = ClientModelSerializer()
    option = OptionsModelSerializer()

    class Meta:
        model = Orders
        fields = ("id", "client", "option", "instructions", "date")
        read_only_fields = ("id", "date")
