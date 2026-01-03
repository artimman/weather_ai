# django_app/config/settings_dev.py

from .settings import *

DEBUG = True

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
