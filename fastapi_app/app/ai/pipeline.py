# fastapi_app/app/ai/pipeline.py

import uuid

from sqlalchemy.orm import Session

from ..services.metrics import compute_wind_chill, compute_heat_index
from ..services.weather_fetcher import fetch_weather_openweather, normalize_weather
from ..models.report import Report
from ..core import AI_PROVIDER, OPENAI_API_KEY
from ..ai.providers import get_provider

async def generate_full_report(location_q: dict, db: Session):
    lat, lon = location_q.get("lat"), location_q.get("lon")

    raw = await fetch_weather_openweather(lat, lon)
    normalized = await normalize_weather(raw)

    current = normalized["current"]
    temp = current.get("temp")
    wind_ms = current.get("wind_speed", 0)
    wind_kph = wind_ms * 3.6

    wc = compute_wind_chill(temp, wind_kph)
    hi = compute_heat_index(temp, current.get("humidity", 0))

    # TRYB BEZ AI
    if AI_PROVIDER in ("none", "", None):
        return {
            "mode": "weather-only",
            "location": location_q.get("name"),
            "metrics": {
                "temperature": temp,
                "wind_kph": round(wind_kph, 1),
                "wind_chill": wc,
                "heat_index": hi,
            },
            "weather": normalized,
        }

    # ===== AI MODE =====

    prompt = f"""
    You are a professional meteorologist.
    Location: {location_q.get("name")}
    Temperature: {temp}°C
    Wind: {wind_kph:.1f} km/h
    Wind chill: {wc}°C
    Heat index: {hi}°C
    """

    provider = get_provider(AI_PROVIDER, OPENAI_API_KEY)
    ai_text = provider.generate(prompt, max_tokens=500, temperature=0.2)

    report = Report(
        report_id=str(uuid.uuid4()),
        location_name=location_q.get("name"),
        raw_payload=normalized,
        summary=ai_text.split("\n\n")[0] if ai_text else "",
        expert_notes=ai_text,
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return {
        "mode": "ai",
        "report_id": report.report_id,
        "summary": report.summary,
    }
