# django_app/config/settings_prod.py

from .settings import *

DEBUG = False

STATIC_ROOT = BASE_DIR / "staticfiles"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    *MIDDLEWARE,
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
