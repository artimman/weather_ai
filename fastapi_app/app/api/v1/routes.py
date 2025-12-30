# fastapi_app/app/api/v1/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .schemas import LocationIn, ReportOut, WeatherOut
from ...services.db import get_db
from ...ai.pipeline import generate_full_report
from ...core.security import get_current_user

router = APIRouter(prefix="/reports", tags=["Weather Reports"])

@router.post(
    "/generate",
    response_model=ReportOut,
    summary="Generate extended AI weather report",
    description="""
Generates a full weather analysis:
- fetch raw weather data
- normalize metrics
- compute expert indexes (wind chill, heat index)
- generate AI summary
- store report in PostgreSQL
"""
)
async def generate_report(
        location: LocationIn,
        user=Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
    # TODO!
    # try:
    #     result = await generate_full_report(location.dict(), db)
    #     return result
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(501, "AI reports disabled (WIP)")


@router.post(
    "/weather",
    response_model=WeatherOut,
    summary="Fetch and compute weather data (no AI)",
)
async def weather_only(
    location: LocationIn,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from ...services.weather_fetcher import fetch_weather_openweather, normalize_weather
    from ...services.metrics import compute_wind_chill, compute_heat_index

    raw = await fetch_weather_openweather(location.lat, location.lon)
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
            "heat_index": compute_heat_index(temp, current.get("humidity", 0)),
        },
        "weather": normalized,
    }
