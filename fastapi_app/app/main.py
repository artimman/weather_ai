# fastapi_app/app/main.py

from app.api.v1.schemas import HealthOut
from fastapi import FastAPI

from .api.v1 import routes as v1_routes

app = FastAPI(
    title="Weather AI Platform",
    description="""
AI-powered weather analytics platform.

Features:
- AI-generated weather reports
- PostgreSQL persistence
- Django Admin panel
- Redis caching
""",
    version="1.0.0",
    contact={
        "name": "Company Name",
        "email": "admin@example.com",
    },
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "JWT authentication handled by Django",
        },
        {
            "name": "Weather Reports",
            "description": "Weather data, metrics and forecasts",
        },
        {"name": "System", "description": "Infrastructure & health endpoints"},
    ],
)

app.include_router(v1_routes.router, prefix="/api/v1")


@app.get(
    "/health",
    tags=["System"],
    response_model=HealthOut,
    summary="Health check",
)
async def health():
    return {"status": "ok"}
