# django_app/accounts/views.py

import logging

import httpx
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from rest_framework_simplejwt.tokens import RefreshToken

LOGIN_URL = f"{settings.DJANGO_API_BASE_URL}/auth/login/"
WEATHER_URL = f"{settings.FASTAPI_API_BASE_URL}/reports/weather"


@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)  # TEMP

    if request.method == "GET":
        return render(request, "auth/login.html")

    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return render(
                request,
                "partials/login_error.html",
                {"error": "Invalid username or password"},
                status=200,  # optional: 401
            )

        login(request, user)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = JsonResponse({"detail": "ok"})
        response["HX-Redirect"] = "/weather/dashboard/"

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite="Lax",
            max_age=60 * 15,
            path="/",
        )

        return response

    except Exception:
        import traceback

        traceback.print_exc()
        logger = logging.getLogger(__name__)
        logger.warning("USERNAME = %s", username)
        return HttpResponse("Internal Server Error", status=500)


def logout_view(request):
    logout(request)  # SESSION
    response = redirect(settings.LOGOUT_REDIRECT_URL)
    response.delete_cookie("access_token")  # JWT
    return response


@login_required
def weather_dashboard(request):
    return render(request, "weather/dashboard.html")


@login_required
def weather_view(request):
    token = request.COOKIES.get("access_token")
    if not token:
        return HttpResponseForbidden("Unauthorized")

    location = request.GET.get("location") or "Warsaw"

    payload = {
        "name": location,
    }

    headers = {"Authorization": f"Bearer {token}"}

    with httpx.Client(timeout=10) as client:
        r = client.post(
            f"{settings.FASTAPI_API_BASE_URL}/reports/weather",
            json=payload,
            headers=headers,
        )

    if r.status_code != 200:
        return render(
            request,
            "partials/weather_error.html",
            {"message": "Weather service unavailable"},
        )

    return render(request, "partials/weather.html", {"data": r.json()})


@login_required
def ai_report_view(request):
    token = request.COOKIES.get("access_token")
    if not token:
        return HttpResponseForbidden("Unauthorized")

    location = request.GET.get("location") or "Warsaw"

    payload = {"name": location}
    headers = {"Authorization": f"Bearer {token}"}

    with httpx.Client(timeout=30) as client:
        r = client.post(
            f"{settings.FASTAPI_API_BASE_URL}/reports/generate",
            json=payload,
            headers=headers,
        )

    # Brak JSON = kontrolowany fallback
    if r.status_code != 200 or not r.content:
        return render(
            request,
            "partials/ai_report_error.html",
            {"message": "AI is unavailable! Please check your account."},
        )

    # Bezpieczne parsowanie JSON
    try:
        data = r.json()

    except ValueError:
        return render(
            request,
            "partials/ai_report_error.html",
            {"message": "Unable to read AI response."},
        )

    # AI wyłączone celowo - pokazujemy pogodę bez AI
    if data.get("mode") == "weather-only":
        return render(
            request,
            "partials/ai_report.html",
            {
                "report": data,
            },
        )

    # AI niedostępne (quota / key / error)
    if data.get("mode") == "ai-disabled":
        return render(
            request,
            "partials/ai_report_error.html",
            {"message": data.get("message", "AI is temporarily unavailable.")},
        )

    # Sukces
    return render(
        request,
        "partials/ai_report.html",
        {
            "report": data,
        },
    )
