from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.authtoken import views
from .menus.views import *
from .orders.views import *

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

menu_router = DefaultRouter()
menu_router.register("menu", MenuListViewSet)
menu_router.register("menus", MenuCreateViewSet)
menu_router.register("option", OptionModelViewSet)
menu_router.register("order", OrderModelViewSet)

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/doc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("admin/", admin.site.urls),
    path("api-token-auth/", views.obtain_auth_token),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/v1/", include(menu_router.urls)),
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
