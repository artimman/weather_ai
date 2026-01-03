# fastapi_app/app/services/weather_fetcher.py

import os

import httpx

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_BASE_URL = os.getenv(
    "OPENWEATHER_BASE_URL",
    "https://api.openweathermap.org/data/2.5",
)


class WeatherProviderError(RuntimeError):
    pass


async def fetch_weather_openweather(lat: float, lon: float) -> dict:
    if not OPENWEATHER_API_KEY:
        raise WeatherProviderError("OPENWEATHER_API_KEY is not configured")

    url = f"{OPENWEATHER_BASE_URL}/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "appid": OPENWEATHER_API_KEY,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()


async def normalize_weather(raw: dict) -> dict:
    return {
        "current": {
            "temp": raw.get("main", {}).get("temp"),
            "humidity": raw.get("main", {}).get("humidity"),
            "wind_speed": raw.get("wind", {}).get("speed"),
            "weather": raw.get("weather", []),
        }
    }
