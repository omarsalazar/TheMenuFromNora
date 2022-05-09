from datetime import datetime
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from CornershopTest.menus.models import Menu, Options
from CornershopTest.menus.serializers import (
    MenuModelSerializer,
    OptionsModelSerializer,
    CreateMenuModelSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny


class MenuListViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    permission_classes = [AllowAny]
    serializer_class = MenuModelSerializer
    queryset = Menu.objects.filter(date=datetime.now())


class MenuCreateViewSet(
    GenericViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateMenuModelSerializer
    queryset = Menu.objects.all()


class OptionModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OptionsModelSerializer
    queryset = Options.objects.all()
