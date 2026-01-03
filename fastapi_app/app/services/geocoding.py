# fastapi_app/app/services/geocoding.py

import os

import httpx
from fastapi import HTTPException

OPENWEATHER_NOMINATIM_URL = os.getenv(
    "OPENWEATHER_NOMINATIM_URL",
    "https://nominatim.openstreetmap.org/search",
)


async def geocode_city(city: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            OPENWEATHER_NOMINATIM_URL,
            params={
                "q": city,
                "format": "json",
                "limit": 1,
            },
            headers={"User-Agent": "weather-app"},
        )

    data = r.json()
    if not data:
        raise HTTPException(404, "City not found")

    return float(data[0]["lat"]), float(data[0]["lon"])
