# django_app/accounts/middleware.py

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthCookieMiddleware:
    COOKIE_NAME = "access_token"

    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        request.user = AnonymousUser()

        token = request.COOKIES.get(self.COOKIE_NAME)
        if token:
            try:
                validated = self.jwt_auth.get_validated_token(token)
                user = self.jwt_auth.get_user(validated)
                request.user = user
            except Exception:
                pass

        return self.get_response(request)
