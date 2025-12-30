# fastapi_app/app/core/config.py

import os

from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
