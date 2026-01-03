# django_app/config/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

# INFO: Pakiet zainstalowany w kontenerze nie widoczny w kodzie aplikacji
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def health(request):
    return JsonResponse({"status": "Ok. You can login now."})


urlpatterns = [
    path("", health, name="index_health"),
    path("admin/", admin.site.urls, name="admin_dashboard"),
    # programmatic auth
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"), # TODO! refresh token
    # frontend (accounts app)
    path("", include("accounts.urls")),
]

# Static for style CSS etc.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)
