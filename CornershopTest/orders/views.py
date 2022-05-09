from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from CornershopTest.orders.models import Orders
from CornershopTest.orders.serializers import OrderModelSerializer


class OrderModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderModelSerializer
    queryset = Orders.objects.all()
