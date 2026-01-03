# django_app/accounts/urls.py

from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("weather/dashboard/", views.weather_dashboard, name="weather_dashboard"),
    path("weather/view/", views.weather_view, name="weather_view"),
    path("ai/report/", views.ai_report_view, name="ai_report"),
]
