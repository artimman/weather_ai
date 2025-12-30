# django_app/config/urls.py

from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

# INFO: Pakiet zainstalowany w kontenerze nie widoczny w kodzie aplikacji
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def health(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("", health),
    path("admin/", admin.site.urls),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
