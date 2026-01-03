# fastapi_app/app/api/v1/routes.py

import logging

from app.ai.pipeline import generate_full_report
from app.api.v1.schemas import LocationIn, ReportResponse, WeatherOut
from app.core.security import get_current_user
from app.services.db import get_db
from app.services.geocoding import geocode_city
from app.services.metrics import compute_heat_index, compute_wind_chill
from app.services.weather_fetcher import fetch_weather_openweather, normalize_weather
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/reports", tags=["Weather Reports"])


@router.post(
    "/generate",
    response_model=ReportResponse,
    summary="Generate AI weather report or weather-only fallback",
    responses={
        401: {"description": "Unauthorized"},
        422: {"description": "Validation error"},
        500: {"description": "Internal error"},
    },
)
async def generate_report(
    location: LocationIn,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    AI_PROVIDER=openai  -> AI report
    AI_PROVIDER=none    -> weather-only fallback
    """
    return await generate_full_report(
        location_q=location.dict(),
        db=db,
    )


@router.post(
    "/weather",
    response_model=WeatherOut,
    summary="Fetch weather data without AI",
    responses={
        401: {"description": "Unauthorized"},
        422: {"description": "Validation error"},
        500: {"description": "Internal error"},
    },
)
async def weather_only(
    location: LocationIn,
    user=Depends(get_current_user),
):
    try:
        lat, lon = await geocode_city(location.name)

        raw = await fetch_weather_openweather(lat, lon)
        normalized = await normalize_weather(raw)

        current = normalized["current"]
        temp = current.get("temp")
        wind_ms = current.get("wind_speed", 0)
        wind_kph = wind_ms * 3.6

        return {
            "location": location.name,
            "metrics": {
                "temperature": temp,
                "wind_kph": round(wind_kph, 1),
                "wind_chill": compute_wind_chill(temp, wind_kph),
                "heat_index": compute_heat_index(
                    temp,
                    current.get("humidity", 0),
                ),
            },
            "weather": normalized,
        }

    except Exception as exc:
        logger = logging.getLogger("uvicorn.error")
        logger.exception("Weather fetch failed: %s", exc)
        raise
